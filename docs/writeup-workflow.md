# Authoring and publishing

## Choose the content type

| Type | Use when | Collection / template |
| --- | --- | --- |
| WRITEUP | A walkthrough, lab, CTF/challenge or reproduction with an observed path | `_writeups/` / `ctf-template.md` |
| NOTE | Short reusable technical knowledge or a reference | `_notes/` / `note-template.md` |
| RESEARCH | Deeper investigation, experiment, analysis or an engineering lesson | `_research/` / `research-template.md` |
| PROJECT | Something actually built or maintained by you | `_projects/` / `project-template.md` |

Choose the primary purpose; a vulnerability reproduction can be a writeup, while investigation of its behavior can be research. No generic Articles collection. Templates are optional outlines, not mandatory narratives. Do not invent results or create sample content to fill an archive.

## Create, write, build

1. Copy the template from `_templates/` into the matching flat collection; create the directory if it has no content yet.
2. Fill title, matching type, original ISO date (`YYYY-MM-DD`) and a unique explicit permalink. Supply only factual optional metadata; omit unknown values. The three new templates default to `published: false`; set true when reviewed. Keep `starred` false/absent unless intentionally featuring the entry.
3. Write Markdown, using relevant H2/H3 sections. The article layout supplies the title; no extra H1 or `legacy_body_header` for new content. Keep commands/output accurate and screenshots under `assets/images/` with descriptive alt text.
4. Build, validate, preview and review changes. Commit/push are user-controlled; pushes to `main` publish through Actions. PRs validate without deployment.

No homepage, archive, platform list, tag index or existing topic index is manually edited. Latest mixes all four types by date. Notes/Research/Projects enter primary navigation automatically when published content exists.

## Filenames, platform and URLs

Writeup source names use lowercase kebab-case:

- TryHackMe: `_writeups/thm-<slug>.md`
- HackTheBox: `_writeups/htb-<slug>.md`
- Define another abbreviation only when real content requires it.

Other types use `_notes/<slug>.md`, `_research/<slug>.md`, `_projects/<slug>.md`. Source names organize the repository; the visible title and platform come from metadata. No platform subdirectories.

New route patterns: `/writeups/<prefixed-source-stem>/`, `/notes/<slug>/`, `/research/<slug>/`, `/projects/<slug>/`. Uncomment/fill the template permalink with a unique stable route. Existing articles retain their exact case-sensitive `/TryHackMe/*.html` permalinks. Do not copy one into new content.

For writeups use `platform`, `source_url`, and known `os`/`difficulty`; omit a source URL when none exists. `parent`, `link`, `machine_url` are obsolete. New content can omit unknown OS/difficulty and optional summary/topics/techniques/tools/updated. Fields such as `starred` and `published` are YAML booleans, not quoted strings. Taxonomy fields are arrays of nonempty strings.

Optional research `references` is an array of `{title: "Source title", url: "https://..."}` objects. Optional project `repository_url`/`demo_url` must be real approved public HTTP(S) destinations. These optional metadata fields are not rendered automatically: include useful links in the Markdown body. Project links do not create a personal profile panel.

`published: false` prevents normal Jekyll output. Future dates are excluded by normal builds and become visible only after a subsequent build on/after that date; no scheduled build was added. `status: draft` omits discovery but does not itself prevent direct page output; use `published: false` for unfinished content. These controls are not confidentiality mechanisms. Research/note status may be draft/published/archived; project status may be active/maintenance/archived. Archived does not mean hidden.

## Map an existing topic

Add supported existing slugs to `topics: [...]` in front matter:
`web-security`, `linux-privilege-escalation`, `credential-attacks`, `enumeration`, `network-forensics`, `reverse-engineering`.

Tags are lightweight descriptors; topics are curated knowledge routes. A tag alone is not evidence for a topic mapping. Related lists, counts and article backlinks update automatically across all four types. New content does not need an entry in the historical `docs/topic-evidence.json`: that record protects the original 20 writeups. Reclassifying an original requires deliberate review of its evidence record.

For a genuinely new topic, define a meaningful scope supported by real published content, create `_topics/<slug>.md` with `title`, stable `slug`, explicit `permalink`, and a factual human-readable `description`, and assign curated topic mappings in that content. The body can explain a useful reading route. Prefer multiple supported documents or clearly meaningful coverage; do not create empty or tag-derived topics. `featured: true` is an intentional editorial choice. Homepage/topic indexes need no manual list edits. This phase adds no new taxonomy or mappings.

## Local checks

Use the existing locked gems, `.ruby-version`, root Gemfile/lock and a repository-local bundle. This checkout uses `docs/vendor/bundle`; fresh root installs may use `vendor/bundle` instead. Do not use the historical `docs/baseline.Gemfile` for normal builds.

```sh
export BUNDLE_PATH="$PWD/docs/vendor/bundle"
export BUNDLE_FROZEN=true JEKYLL_ENV=production TZ=UTC
bundle exec jekyll build --trace --baseurl ""
python3 docs/verify-writeups.py _site
python3 docs/verify-phase4.py _site
python3 docs/verify-publication.py
bundle exec ruby docs/verify-authoring.rb
git diff --check
bundle exec jekyll serve --host 127.0.0.1 --baseurl ""
```

The plugin validates shared title/type/date, explicit local permalink, taxonomy arrays, boolean starred, optional summary and HTTP(S) link/reference shapes. It validates curated topic membership and output-route uniqueness. Preserve the original date; never replace it with Git/build timestamps.

`verify-writeups.py` preserves all 20 originals against the immutable manifest, allowing only approved Liquid substitutions and exact Phase 6 repairs recorded in `editorial-corrections.json`. It checks metadata, images/hashes, all generated links/anchors, routes and publication-aware writeup/platform archives. New writeups, including the first real HTB entry, are supported. `verify-phase2.py` is a compatibility wrapper for that same check.

`verify-phase4.py` checks actual published homepage/activity/navigation/topics and the original curated evidence without freezing the future content/topic counts. `verify-authoring.rb` builds all four real templates in an isolated ignored source, verifies article/archive/Latest/topic discovery, excludes draft/future fixtures, checks invalid metadata, and removes its entire disposable source/output. No fake content enters the real collections. No new dependencies.

Optional `docs/verify-browser.py` uses an existing isolated Chromium/debugging instance and local preview; evidence stays under ignored `.jekyll-cache/phase4/`. Review keyboard focus, code/table scrolling, image legibility and mobile pages before publication. No browser runtime dependency is added to the site.

See [publication.md](publication.md) for Actions behavior, manual controls and source-based rollback. Historical architecture and phase reports remain under `docs/`.
