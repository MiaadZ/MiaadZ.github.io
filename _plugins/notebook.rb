# Build-only notebook indexes, validation and semantic HTML presentation.
# Topics and discovery indexes are derived from published Markdown metadata.
require "cgi"
require "date"
require "uri"

module Notebook
  class Foundation < Jekyll::Generator
    safe false
    priority :normal

    def generate(site)
      collection_types = {"writeups" => "writeup", "notes" => "note", "projects" => "project"}
      entries = collection_types.keys.flat_map { |name| site.collections.fetch(name).docs }
      # Check required editorial fields before Publisher asks Document#date,
      # which can otherwise replace a missing date with the build time.
      entries.reject { |entry| entry.data["published"] == false || entry.data["status"] == "draft" }.each do |entry|
        unless entry.data["type"] == collection_types.fetch(entry.collection.label)
          raise Jekyll::Errors::FatalException, "Invalid content type: #{entry.path}"
        end
        if !entry.data["title"].is_a?(String) || entry.data["title"].strip.empty?
          raise Jekyll::Errors::FatalException, "Missing title: #{entry.path}"
        end
        if entry.data["date"].nil?
          raise Jekyll::Errors::FatalException, "Missing date: #{entry.path}"
        end
      end
      entries.each { |entry| entry.data["published"] = false if entry.data["status"] == "draft" }
      entries = entries.select { |entry| site.publisher.publish?(entry) && entry.data["status"] != "draft" }
      entries.each { |entry| validate_metadata!(entry) }
      site.config["notebook_entries"] = entries.sort_by do |entry|
        [-Date.parse(entry.data["date"].to_s).jd, entry.data["title"].to_s.downcase, entry.url]
      end
      site.pages.reject! { |page| page.data["generated_topic"] }
      topics = entries.flat_map { |entry| entry.data.fetch("topics", []) }.uniq.sort.map do |slug|
        page = Jekyll::PageWithoutAFile.new(site, site.source, "topics/#{slug}", "index.html")
        page.data.merge!("layout" => "topic", "title" => slug.split("-").map(&:capitalize).join(" "),
                         "slug" => slug, "nav_section" => "topics", "generated_topic" => true,
                         "description" => site.data.dig("topics", slug, "description"),
                         "entry_count" => entries.count { |entry| Array(entry.data["topics"]).include?(slug) })
        site.pages << page
        page
      end
      site.config["notebook_topics"] = topics
      counts = collection_types.transform_values { |type| entries.count { |entry| entry.data["type"] == type } }
      site.config["notebook_collection_counts"] = counts.merge("topics" => topics.length)
      site.config["notebook_tags"] = entries.flat_map { |entry| Array(entry.data["tags"]) }.uniq.sort_by(&:downcase)
      slugs = {}
      site.config["notebook_tags"].each do |tag|
        slug = Jekyll::Utils.slugify(tag)
        if slugs.key?(slug) && slugs[slug] != tag
          raise Jekyll::Errors::FatalException, "Colliding tag slugs: #{tag}"
        end
        slugs[slug] = tag
      end
      site.pages.select { |page| page.data["archive_collection"] }.each do |page|
        unless %w[writeups notes projects].include?(page.data["archive_collection"])
          raise Jekyll::Errors::FatalException, "Invalid archive selector: #{page.path}"
        end
      end
      urls = (site.pages + site.collections.values.flat_map(&:docs)).group_by(&:url)
      duplicates = urls.select { |_url, documents| documents.length > 1 }.keys
      raise Jekyll::Errors::FatalException, "Duplicate routes: #{duplicates.join(', ')}" unless duplicates.empty?
    end
    private

    def validate_metadata!(entry)
      data = entry.data
      invalid = lambda do |field|
        raise Jekyll::Errors::FatalException, "Invalid #{field}: #{entry.path}"
      end
      route = data["permalink"]
      invalid.call("permalink") if route && !(route.is_a?(String) && route.start_with?("/") && !route.start_with?("//") && !route.match?(/[?#\\\s]/))
      %w[tags topics].each do |field|
        next unless data.key?(field)
        values = data[field]
        invalid.call(field) unless values.is_a?(Array) && values.all? { |v| v.is_a?(String) && !v.strip.empty? }
      end
      if data.key?("topics")
        topics = data["topics"]
        invalid.call("topics") unless topics.uniq == topics && topics.all? { |v| v.match?(/\A[a-z0-9]+(?:-[a-z0-9]+)*\z/) }
      end
      begin
        Date.iso8601(data["date"].to_s[0, 10])
      rescue ArgumentError
        invalid.call("date")
      end
      invalid.call("starred") unless [true, false].include?(data.fetch("starred", false))
      invalid.call("status") if data.key?("status") && !data["status"].is_a?(String)
      invalid.call("summary") if data.key?("summary") && !data["summary"].is_a?(String)
      if data["type"] == "writeup"
        invalid.call("platform") unless data["platform"].is_a?(String) && !data["platform"].strip.empty?
      end
      %w[source_url repository_url demo_url].each do |field|
        next if !data.key?(field) || data[field] == ""
        invalid.call(field) unless valid_url?(data[field])
      end
    end

    def valid_url?(value)
      return false unless value.is_a?(String)
      uri = URI.parse(value)
      %w[http https].include?(uri.scheme) && uri.host && !uri.userinfo
    rescue URI::InvalidURIError
      false
    end
  end

  module Filters
    # Reposition the existing generated H1 into the article header without
    # changing its text, ID, link or original Markdown bytes.
    def notebook_heading(html)
      html[/\A\s*(<h1\b[^>]*>.*?<\/h1>)/m, 1].to_s
    end

    def notebook_article_body(html)
      html.sub(/\A\s*<h1\b[^>]*>.*?<\/h1>/m, "")
    end

    def notebook_source_url(value)
      uri = URI.parse(value.to_s)
      value if %w[http https].include?(uri.scheme) && uri.host && !uri.userinfo
    rescue URI::InvalidURIError
      nil
    end

    # Operates on generated HTML, never on Markdown source or fenced code.
    # Kramdown-generated headings use these exact heading/id attributes.
    def notebook_toc(html, label = "Contents")
      headings = html.scan(/<h([2-4]) id="([^"]+)">(.*?)<\/h\1>/m)
      return "" if headings.empty?
      links = headings.map do |level, id, title|
        text = CGI.escapeHTML(CGI.unescapeHTML(title.gsub(/<[^>]*>/, "")))
        %(<li class="level-#{level}"><a href="##{CGI.escapeHTML(CGI.unescapeHTML(id))}">#{text}</a></li>)
      end.join
      label = "Contents" if label.to_s.strip.empty?
      %(<details class="toc"><summary>#{CGI.escapeHTML(label.to_s)}</summary><nav aria-label="On this page"><ul>#{links}</ul></nav></details>)
    end

    def notebook_overflow(html)
      html.gsub(/<pre\b[^>]*>.*?<\/pre>/m) do |block|
        %(<div class="scroll-region" role="region" aria-label="Scrollable code or command output" tabindex="0">#{block}</div>)
      end.gsub(/<table\b[^>]*>.*?<\/table>/m) do |block|
        %(<div class="scroll-region" role="region" aria-label="Scrollable table" tabindex="0">#{block}</div>)
      end
    end
  end
end

Liquid::Template.register_filter(Notebook::Filters)
