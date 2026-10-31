# Build disposable content to protect the copy-template → publish workflow.
require "jekyll"
require "tmpdir"
require "fileutils"
require "date"
require "yaml"

root = Dir.pwd
FileUtils.mkdir_p(File.join(root, ".jekyll-cache"))
Dir.mktmpdir("authoring-", File.join(root, ".jekyll-cache")) do |source|
  %w[_config.yml _data _layouts _includes _sass assets _plugins _writeups _notes _projects _templates].each do |name|
    FileUtils.cp_r(name, source) if File.exist?(name)
  end
  Dir["*.md", "*.html"].each { |path| FileUtils.cp(path, source) }
  {"writeups" => "ctf", "notes" => "note", "projects" => "project"}.each do |collection, template|
    directory = File.join(source, "_#{collection}")
    FileUtils.mkdir_p(directory)
    text = File.read("_templates/#{template}-template.md")
    data = YAML.safe_load(text.split("---", 3)[1], permitted_classes: [Date, Time])
    data.merge!("title" => "Authoring fixture", "date" => Date.today, "published" => true,
                "topics" => ["new-automatic-topic"], "tags" => ["fixture"])
    data["platform"] = "Custom Lab" if collection == "writeups"
    body = text.split("---", 3)[2] + "\n## Evidence\n\n```text\nfixture\n```\n"
    File.write(File.join(directory, "check-fixture.md"), data.to_yaml + "---\n" + body)
    {"hidden" => {"published" => false}, "future" => {"date" => Date.today + 365},
     "draft" => {"status" => "draft"}}.each do |kind, changes|
      File.write(File.join(directory, "#{kind}-fixture.md"), data.merge(changes).to_yaml + "---\n" + body)
    end
  end
  config = Jekyll.configuration("source" => source, "destination" => File.join(source, "_site"),
                                "quiet" => true, "disable_disk_cache" => true)
  site = Jekyll::Site.new(config)
  site.process
  home = File.read(File.join(site.dest, "index.html"))
  topic = File.read(File.join(site.dest, "topics/new-automatic-topic/index.html"))
  %w[writeups notes projects].each do |collection|
    route = "/#{collection}/check-fixture/"
    raise "Article missing: #{route}" unless File.file?(File.join(site.dest, route, "index.html"))
    archive = File.read(File.join(site.dest, collection, "index.html"))
    [archive, home, topic].each { |html| raise "Discovery missing #{route}" unless html.include?(route) }
    %w[hidden future draft].each do |kind|
      route = "/#{collection}/#{kind}-fixture/"
      raise "Draft/future page leaked" if File.exist?(File.join(site.dest, route, "index.html"))
      raise "Draft/future discovery leaked" if home.include?(route) || topic.include?(route)
    end
  end
  generator = Notebook::Foundation.new
  entry = site.collections["notes"].docs.find { |doc| doc.basename_without_ext == "check-fixture" }
  {"title" => [], "date" => "not-a-date", "tags" => "tag", "topics" => ["../bad"],
   "starred" => "false", "permalink" => "//example.com/", "demo_url" => "javascript:alert(1)"}.each do |field, value|
    original = entry.data.dup
    entry.data[field] = value
    begin
      generator.generate(site)
      raise "Invalid #{field} accepted"
    rescue Jekyll::Errors::FatalException
      # Expected metadata rejection.
    ensure
      entry.data.replace(original)
    end
  end
end
puts "PASS: three templates publish automatically; new topics, archives, Latest, draft/future exclusion and invalid metadata"
