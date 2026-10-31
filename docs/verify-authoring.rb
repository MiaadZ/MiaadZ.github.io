#!/usr/bin/env ruby
# Full new-content builds in an isolated ignored source tree; no published fixtures.
# Run from repository root: bundle exec ruby docs/verify-authoring.rb
require "jekyll"
require "yaml"
require "date"
require "json"
require "tmpdir"
require "fileutils"
require "open3"

ROOT = File.realpath(Dir.pwd)
CACHE = File.join(ROOT, ".jekyll-cache", "phase7")
FileUtils.mkdir_p(CACHE)
source = Dir.mktmpdir("authoring-", CACHE)

def check(condition, message)
  raise message unless condition
end

def front_matter(path)
  text = File.read(path)
  match = text.match(/\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)/m)
  [YAML.safe_load(match[1], permitted_classes: [Date, Time]), text[match.end(0)..]]
end

begin
  # Copy only build sources and local verification inputs; never bundles or .git.
  %w[_config.yml _data _layouts _includes _sass assets _plugins _writeups _notes _research _projects _topics _templates .github].each do |name|
    FileUtils.cp_r(File.join(ROOT, name), source) if File.exist?(File.join(ROOT, name))
  end
  Dir[File.join(ROOT, "*.md")].each { |path| FileUtils.cp(path, source) }
  FileUtils.mkdir_p(File.join(source, "docs"))
  Dir[File.join(ROOT, "docs", "*")].select { |p| File.file?(p) }.each { |p| FileUtils.cp(p, File.join(source, "docs")) }
  routes = {}
  hidden = []
  templates = {"writeups" => "ctf", "notes" => "note", "research" => "research", "projects" => "project"}
  templates.each do |collection, template|
    directory = File.join(source, "_#{collection}")
    FileUtils.mkdir_p(directory)
    data, body = front_matter(File.join(ROOT, "_templates", "#{template}-template.md"))
    data.merge!("title" => "TEST FIXTURE #{template}", "date" => Date.today,
                "summary" => "Isolated authoring regression fixture; never published.",
                "published" => true, "tags" => ["authoring-fixture"], "topics" => ["web-security"],
                "permalink" => "/#{collection}/phase7-fixture/", "starred" => false)
    if collection == "writeups"
      data.merge!("platform" => "HackTheBox", "source_url" => "https://example.invalid/lab")
    end
    data["references"] = [{"title" => "Fixture reference", "url" => "https://example.invalid/reference"}] if collection == "research"
    data["repository_url"] = "https://example.invalid/repository" if collection == "projects"
    filename = collection == "writeups" ? "htb-phase7-fixture.md" : "phase7-fixture.md"
    path = File.join(directory, filename)
    File.write(path, data.to_yaml + "---\n" + body)
    routes[collection] = data["permalink"]
    {"draft" => {"published" => false}, "future" => {"date" => Date.today + 365}}.each do |kind, changes|
      unpublished = data.merge(changes).merge("title" => "TEST FIXTURE #{kind} #{template}", "permalink" => "/#{collection}/phase7-#{kind}/")
      name = collection == "writeups" ? "htb-phase7-#{kind}.md" : "phase7-#{kind}.md"
      File.write(File.join(directory, name), unpublished.to_yaml + "---\n" + body)
      hidden << unpublished["permalink"]
    end
  end
  # Test intentional creation of a new curated route without touching an index.
  # This topic and its mapping exist only inside the disposable source.
  topic = {"title" => "TEST FIXTURE topic", "slug" => "authoring-fixture", "description" => "Isolated topic discovery test; never published.", "featured" => true, "permalink" => "/topics/authoring-fixture/"}
  File.write(File.join(source, "_topics", "authoring-fixture.md"), topic.to_yaml + "---\n")
  # One meaningful supporting document also exercises singular topic counts.
  ["notes"].each do |collection|
    name = "phase7-fixture.md"
    path = File.join(source, "_#{collection}", name)
    data, body = front_matter(path)
    data["topics"] << "authoring-fixture"
    File.write(path, data.to_yaml + "---\n" + body)
  end
  config = Jekyll.configuration({"source" => source, "destination" => File.join(source, "_site"), "quiet" => true, "disable_disk_cache" => true, "future" => false, "unpublished" => false})
  site = Jekyll::Site.new(config)
  site.process
  home = File.read(File.join(site.dest, "index.html"))
  topic_html = File.read(File.join(site.dest, "topics", "web-security", "index.html"))
  new_topic = File.read(File.join(site.dest, "topics", "authoring-fixture", "index.html"))
  latest = home[/<section[^>]*aria-labelledby="latest-title".*?<\/section>/m]
  check(latest, "Missing Latest section")
  routes.each do |collection, route|
    article = File.read(File.join(site.dest, route, "index.html"))
    archive = File.read(File.join(site.dest, collection, "index.html"))
    check(article.include?('<article class="article">') && article.scan(/<h1\b/).length == 1, "Shared article layout missing: #{collection}")
    check(archive.include?("href=\"#{route}\"") && latest.include?("href=\"#{route}\""), "Missing archive/Latest discovery: #{collection}")
    check(topic_html.include?("href=\"#{route}\""), "Missing curated topic mapping: #{collection}")
    check(new_topic.include?("href=\"#{route}\"") == (collection == "notes"), "Unsupported new topic mapping: #{collection}")
    check(article.include?('href="/topics/web-security/"') && home.include?("href=\"/#{collection}/\""), "Missing topic backlink or conditional navigation")
  end
  check(new_topic.include?("1 entry in the notebook"), "Singular topic count failed")
  htb = File.read(File.join(site.dest, "hackthebox", "index.html"))
  check(htb.include?(routes["writeups"]), "New platform entry requires manual index update")
  check(!Dir.glob(File.join(site.dest, "_templates", "**", "*")).any?, "Templates published")
  hidden.each do |route|
    check(!File.exist?(File.join(site.dest, route, "index.html")), "Draft/future output leaked: #{route}")
    check(!latest.include?(route) && !topic_html.include?(route), "Draft/future discovery leaked")
  end
  # Run the real preservation/route/archive checks against the augmented site.
  %w[verify-writeups.py verify-phase4.py].each do |script|
    output, status = Open3.capture2e({"BUNDLE_PATH" => File.expand_path(ENV.fetch("BUNDLE_PATH", "vendor/bundle"), ROOT), "BUNDLE_GEMFILE" => File.join(ROOT, "Gemfile")}, "python3", File.join(source, "docs", script), site.dest, chdir: source)
    check(status.success?, "New content breaks #{script}:\n#{output}")
  end
  # A real file missing its editorial date must not inherit the build time.
  missing_date = File.join(source, "_notes", "phase7-missing-date.md")
  File.write(missing_date, {"title" => "TEST FIXTURE missing date", "type" => "note", "permalink" => "/notes/phase7-missing-date/"}.to_yaml + "---\n")
  begin
    Jekyll::Site.new(config).process
    raise "Missing source date silently accepted"
  rescue Jekyll::Errors::FatalException => error
    check(error.message.include?("Missing date"), "Unexpected missing-date error: #{error.message}")
  ensure
    File.delete(missing_date)
  end
  # Invalid author metadata must fail before publication, across all four types.
  rejected = 0
  invalid_cases = [
    ["notes", "title", []], ["notes", "date", nil], ["notes", "tags", "one-tag"],
    ["notes", "topics", ["nonexistent-fixture-topic"]], ["notes", "type", "project"],
    ["research", "references", [{"title" => "Invalid", "url" => "javascript:alert(1)"}]],
    ["research", "references", "invalid"], ["research", "starred", "false"],
    ["projects", "repository_url", "javascript:alert(1)"], ["projects", "demo_url", "https://user:password@example.invalid/"],
    ["projects", "summary", []], ["projects", "permalink", "//example.invalid/"],
    ["writeups", "platform", ""], ["writeups", "source_url", "javascript:alert(1)"]
  ]
  invalid_cases.each do |collection, field, value|
    entry = site.collections[collection].docs.find { |d| d.url == routes[collection] }
    backup = entry.data.dup
    entry.data[field] = value
    begin
      Notebook::Foundation.new.generate(site)
      raise "Invalid #{collection}/#{field} was accepted"
    rescue Jekyll::Errors::FatalException
      rejected += 1
    ensure
      entry.data.replace(backup)
    end
  end
  result = {"published_types" => templates.keys, "hidden_fixtures" => hidden.length, "invalid_metadata_rejected" => rejected, "new_topic_discovery" => true, "full_verifiers_pass" => true, "all_pass" => true, "source_removed" => true}
  File.write(File.join(CACHE, "authoring-results.json"), JSON.pretty_generate(result) + "\n")
  puts "PASS: four template-based full article builds, archives/Latest/navigation/topics and new HTB discovery; eight drafts/future entries excluded; #{rejected} invalid metadata cases rejected; no index edits"
ensure
  FileUtils.remove_entry(source) if File.directory?(source)
end
