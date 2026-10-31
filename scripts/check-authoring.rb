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
    data["tags"] += ["fixture", "fixture-third"] if collection == "writeups"
    data["tags"] << "fixture-rare" if collection == "notes"
    data["platform"] = "Custom Lab" if collection == "writeups"
    body = text.split("---", 3)[2] + "\n## Evidence\n\n```text\nfixture\n```\n"
    File.write(File.join(directory, "check-fixture.md"), data.to_yaml + "---\n" + body)
    {"hidden" => {"published" => false}, "future" => {"date" => Date.today + 365},
     "draft" => {"status" => "draft"}}.each do |kind, changes|
      File.write(File.join(directory, "#{kind}-fixture.md"), data.merge(changes).merge("tags" => ["hidden-only-#{kind}"], "topics" => ["hidden-only-#{kind}"]).to_yaml + "---\n" + body)
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
  baseline = Jekyll::Site.new(Jekyll.configuration("source" => root, "quiet" => true, "disable_disk_cache" => true))
  baseline.read
  generator.generate(baseline)
  %w[writeups notes projects].each do |collection|
    expected = baseline.config["notebook_collection_counts"][collection] + 1
    raise "Incorrect published #{collection} count" unless site.config["notebook_collection_counts"][collection] == expected
  end
  raise "Hidden topics counted" unless site.config["notebook_topics"].length == baseline.config["notebook_topics"].length + 1
  raise "Hidden/duplicate tools counted" unless site.config["notebook_tags"].length == baseline.config["notebook_tags"].length + 3
  generated = site.config["notebook_topics"].find { |page| page.data["slug"] == "new-automatic-topic" }
  raise "Incorrect topic membership/tags" unless generated.data.values_at("entry_count", "representative_tags") == [3, %w[fixture fixture-rare fixture-third]]
  status = Liquid::Template.parse(File.read("_layouts/home.html")[/<ul class="notebook-status".*?<\/ul>/m])
  [0, 1, 2].each do |count|
    html = status.render!("counts" => {"projects" => count, "writeups" => count, "topics" => count}, "tools" => count)
    labels = html.scan(/<li>(.*?)<\/li>/m).flatten.map(&:strip)
    expected = count.zero? ? [] : %w[Project Writeup Topic Tool].map { |name| "#{count} #{name}#{count == 1 ? '' : 's'}" }
    raise "Status zero/plural rules failed" unless labels == expected
  end
  fixtures = site.collections.values.flat_map(&:docs).select { |doc| doc.basename_without_ext == "check-fixture" }
  fixtures.each { |doc| doc.data["published"] = false }
  generator.generate(site)
  raise "Removed entries still counted" unless site.config["notebook_collection_counts"] == baseline.config["notebook_collection_counts"] && site.config["notebook_tags"] == baseline.config["notebook_tags"]
  fixtures.each { |doc| doc.data["published"] = true }
  generator.generate(site)
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
puts "PASS: three templates publish automatically; new topics, archives, Latest, draft/future exclusion and invalid metadata; dynamic counts, zero/plural labels and representative tags"
