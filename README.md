# S3Z4R Security Notebook

A Markdown-first Jekyll notebook: technical writeups, curated topic routes and an understated systems/security identity.

## Local build
Use Ruby 3.4.10 and the root Gemfile/Gemfile.lock. Jekyll 4.4.1 is the only direct dependency. Follow AGENTS.md for local dependency actions; new dependencies need approval.

With the existing approved bundle:
```sh
BUNDLE_FROZEN=true BUNDLE_PATH="$PWD/docs/vendor/bundle" bundle exec jekyll build --trace
python3 docs/verify-writeups.py _site
python3 docs/verify-phase2.py _site
python3 docs/verify-phase4.py _site
git diff --check
```
Use vendor/bundle instead if the root bundle was installed there. docs/baseline.Gemfile is for historical theme reproduction only.
Preservation checks require the original Git objects named in docs/legacy-manifest.yml.

## Content
- All 20 original writeups live in flat _writeups/ with preserved /TryHackMe/*.html URLs.
- Six curated _topics/ routes connect actual content. Tags remain an independent lightweight index at /tools/.
- Latest automatically combines published writeups, notes, research and projects.
- Writeups and Topics are always in primary navigation; other types appear when published content exists.
- Empty collection archives remain available; no sample Notes/Research/Projects were added.
- The approved platform-neutral template is _templates/ctf-template.md.
- See [authoring workflow](docs/writeup-workflow.md) for names, metadata, topics and local checks.
- Keep docs/legacy-manifest.yml immutable.

## Presentation and build
The site uses five owned layouts, local Sass, system fonts and no frontend JavaScript, trackers, remote fonts or external badge assets.
Brief CSS identity effects respect reduced motion. Articles remain calm, with accessible code/table overflow.
_plugins/notebook.rb handles published indexes/counts, validation and semantic title/TOC/overflow helpers.
docs/, AGENTS.md, dependencies and editor/build artifacts are excluded from generated output.

The [Phase 4 report](docs/phase4-report.md) records the exact narrative, topic evidence, browser/native-400%-zoom results, file accounting and the recommendation for a future custom Actions build. No workflow or deployment was configured.
[Phase 2](docs/phase2-report.md) and [Phase 3](docs/phase3-report.md) reports remain historical evidence. No commit, push or deployment was performed.
