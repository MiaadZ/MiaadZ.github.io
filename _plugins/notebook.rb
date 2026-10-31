# Build-only notebook indexes, validation and semantic HTML presentation.
# All editorial content now comes from normalized collections; no legacy aliases.
require "cgi"
require "date"
require "uri"

module Notebook
  class Foundation < Jekyll::Generator
    safe false
    priority :normal

    def generate(site)
      collection_types = {"writeups" => "writeup", "notes" => "note", "research" => "research", "projects" => "project"}
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
      entries = entries.select { |entry| site.publisher.publish?(entry) && entry.data["status"] != "draft" }
      entries.each { |entry| validate_metadata!(entry) }
      site.config["notebook_entries"] = entries.sort_by do |entry|
        [-Date.parse(entry.data["date"].to_s).jd, entry.data["title"].to_s.downcase, entry.url]
      end
      topics = site.collections.fetch("topics").docs.select { |topic| site.publisher.publish?(topic) }
      site.config["notebook_topics"] = topics.sort_by { |topic| [topic.data["title"].to_s.downcase, topic.data["slug"].to_s] }
      topic_slugs = topics.map { |topic| topic.data["slug"] }
      if topic_slugs.uniq.length != topic_slugs.length || topic_slugs.any? { |slug| !slug.is_a?(String) || !slug.match?(/\A[a-z0-9]+(?:-[a-z0-9]+)*\z/) }
        raise Jekyll::Errors::FatalException, "Missing, duplicate or invalid topic slug"
      end
      entries.each do |entry|
        assigned = entry.data.fetch("topics", [])
        unless assigned.is_a?(Array) && assigned.uniq == assigned && (assigned - topic_slugs).empty?
          raise Jekyll::Errors::FatalException, "Invalid topic references: #{entry.path}"
        end
      end
      topics.each do |topic|
        if topic.data["description"].to_s.strip.empty?
          raise Jekyll::Errors::FatalException, "Missing topic scope: #{topic.path}"
        end
        topic.data["entry_count"] = entries.count { |entry| Array(entry.data["topics"]).include?(topic.data["slug"]) }
        if topic.data["entry_count"].zero?
          raise Jekyll::Errors::FatalException, "Topic has no published supporting content: #{topic.path}"
        end
      end
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
        unless %w[writeups notes research projects topics].include?(page.data["archive_collection"])
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
      invalid.call("permalink") unless route.is_a?(String) && route.start_with?("/") && !route.start_with?("//") && !route.match?(/[?#\\\s]/)
      %w[tags topics techniques tools].each do |field|
        next unless data.key?(field)
        values = data[field]
        invalid.call(field) unless values.is_a?(Array) && values.all? { |v| v.is_a?(String) && !v.strip.empty? }
      end
      invalid.call("starred") unless [true, false].include?(data.fetch("starred", false))
      invalid.call("summary") if data.key?("summary") && !data["summary"].is_a?(String)
      if data["type"] == "writeup"
        invalid.call("platform") unless data["platform"].is_a?(String) && !data["platform"].strip.empty?
      end
      %w[source_url repository_url demo_url].each do |field|
        next if !data.key?(field) || data[field] == ""
        invalid.call(field) unless valid_url?(data[field])
      end
      if data.key?("references")
        references = data["references"]
        invalid.call("references") unless references.is_a?(Array) && references.all? do |ref|
          ref.is_a?(Hash) && ref["title"].is_a?(String) && !ref["title"].strip.empty? && valid_url?(ref["url"])
        end
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
