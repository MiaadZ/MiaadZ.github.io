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
      entries = %w[writeups notes research projects].flat_map { |name| site.collections.fetch(name).docs }
      entries.each do |entry|
        unless %w[writeup note research project].include?(entry.data["type"])
          raise Jekyll::Errors::FatalException, "Invalid content type: #{entry.path}"
        end
        if entry.data["title"].to_s.strip.empty?
          raise Jekyll::Errors::FatalException, "Missing title: #{entry.path}"
        end
        if entry.data["date"].nil?
          raise Jekyll::Errors::FatalException, "Missing date: #{entry.path}"
        end
      end
      site.config["notebook_entries"] = entries.sort_by do |entry|
        [-Date.parse(entry.data["date"].to_s).jd, entry.data["title"].to_s.downcase, entry.url]
      end
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
