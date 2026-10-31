# S3Z4R Security Notebook

A Markdown-first technical security notebook: writeups, notes, research, real projects and curated knowledge routes. Jekyll, repository-owned layouts/Sass, no frontend JavaScript or tracking.

## Where things live

| Directory | Purpose |
| --- | --- |
| `_writeups/` | Flat lab/CTF/challenge walkthroughs; existing public URLs preserved |
| `_notes/`, `_research/`, `_projects/` | Reusable knowledge, deeper analysis, authored tools/projects |
| `_topics/` | Curated routes connecting published content |
| `_templates/` | Unpublished authoring scaffolds |
| `_layouts/`, `_includes/`, `_sass/`, `assets/` | Shared presentation and local assets |
| `docs/` | Authoring, validation, architecture and historical reports; excluded from publication |

## Add content

1. Copy the matching `_templates/*-template.md` into its collection. Writeups use `ctf-template.md`: `thm-<slug>.md` for TryHackMe or `htb-<slug>.md` for HackTheBox. Other types use `<slug>.md`.
2. Fill factual front matter: title, type, original ISO date, unique explicit permalink, plus known metadata. Platform is metadata, not a folder or visible-title prefix. New templates start with `published: false`; set true when ready.
3. Write Markdown. The shared article layout supplies the title. Attach existing curated topic slugs only when supported by the content.
4. Build, validate and review locally; then commit/push through the normal review process.

Homepage, archives, platform views, Latest, navigation and existing topic lists update automatically. New curated topics are deliberate editorial work; no manual article index is maintained. See the concise [authoring/type guide](docs/writeup-workflow.md).

## Run locally

Use `.ruby-version`, `Gemfile` and `Gemfile.lock`. Choose the existing local bundle path (`docs/vendor/bundle` in this checkout, or `vendor/bundle` for a fresh root install):

```sh
export BUNDLE_PATH="$PWD/docs/vendor/bundle"
export BUNDLE_FROZEN=true JEKYLL_ENV=production TZ=UTC
# Only if the declared locked gems are not installed:
# bundle install
bundle exec jekyll serve --host 127.0.0.1 --baseurl ""
```

## Validate

```sh
bundle exec jekyll build --trace --baseurl ""
python3 docs/verify-writeups.py _site
python3 docs/verify-phase4.py _site
python3 docs/verify-publication.py
bundle exec ruby docs/verify-authoring.rb
git diff --check
```

Run these in the same environment as the local commands above. The authoring regression creates and removes isolated fixtures under ignored `.jekyll-cache/`; no sample content is published. Preservation checks require full Git history and the original objects named in `docs/legacy-manifest.yml`. Keep that manifest immutable. Optional browser QA: `docs/verify-browser.py` (existing local Chromium; no frontend dependency).

## Publishing

GitHub Actions builds the locked Jekyll environment with `_plugins/notebook.rb`, uploads `_site` as a Pages artifact and deploys it. PRs targeting `main` validate only; pushes to `main` publish after checks. Manual runs default to validation; deployment requires `deploy: true` on `main`.

No output branch, generated HTML commits, custom tokens or manual homepage/archive edits. See [publication/rollback runbook](docs/publication.md). `AGENTS.md` defines agent permissions; commits and publication remain user-controlled.
