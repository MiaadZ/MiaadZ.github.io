# S3Z4R Security Notebook

Writeups, practical notes and things I build. Custom Jekyll layouts, local assets,
no frontend JavaScript or tracking.

## Structure

- `_writeups/`: flat lab/CTF/challenge Markdown (`thm-<slug>.md`, `htb-<slug>.md`).
- `_notes/`, `_projects/`: create these folders when publishing the first entry.
- `_templates/`: copy-and-edit starting points for the three content types.
- `_layouts/`, `_includes/`, `_sass/`, `assets/`: presentation and images.
- `_plugins/`, `scripts/`: automatic indexes and publishing checks.

## Write and publish

Copy a template to its collection. Fill title and date (`YYYY-MM-DD`), and
platform for a writeup. Omit unknown optional fields. Write Markdown, remove
irrelevant headings and set `published: true` when ready.

The filename generates the URL. Keep it stable after publication; an optional
`permalink` can preserve an older URL. Existing writeup permalinks stay intact.
Use `published: false` for drafts; future dates are withheld automatically.

Optional metadata:

- `summary`, `tags`, `starred: true` (Featured).
- `topics: [web-security, linux-privilege-escalation]`: any lowercase hyphenated
  subject. Topic pages, labels, counts and links generate automatically.
- Writeups: `source_url`, `os`, `difficulty`, `toc: true`.
- Projects: `status`, `repository_url`, `demo_url`.

Use `/assets/images/<entry>/` for screenshots. Wrap code containing Liquid
syntax in `{% raw %}` / `{% endraw %}`. The layout supplies the article title.

Push to `main` → Actions validates and builds → GitHub Pages deploys.
Archives, Latest, Featured and Topics update automatically. Notes and Projects
enter navigation when their first published entry exists. PRs validate only.

## Local preview and checks

Use the Ruby version in `.ruby-version` and Bundler from `Gemfile.lock`.

```sh
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll serve
```

Before pushing, optionally run the same checks as CI:

```sh
JEKYLL_ENV=production bundle exec jekyll build
python3 scripts/check-site.py _site
bundle exec ruby scripts/check-authoring.rb
git diff --check
```
