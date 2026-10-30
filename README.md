# S3Z4R Security Notebook

A Markdown-first Jekyll security notebook. All 20 existing writeups now live in the flat _writeups collection with normalized metadata and preserved public URLs.

## Local build
Use Ruby 3.4.10 and the root Gemfile/Gemfile.lock. Jekyll 4.4.1 is the only direct target dependency. Follow AGENTS.md for approved local dependency actions; new dependencies need approval.

With the existing approved bundle:
```sh
BUNDLE_FROZEN=true BUNDLE_PATH="$PWD/docs/vendor/bundle" bundle exec jekyll build --trace
python3 docs/verify-writeups.py _site
git diff --check
```

Use vendor/bundle instead if the root bundle was installed there. docs/baseline.Gemfile is for reproducing the historical theme baseline only.

## Content and source
- _writeups/ is flat: thm-<slug>.md and, when authored, htb-<slug>.md.
- Platform is metadata, never a source directory.
- Explicit permalinks preserve all 20 original /TryHackMe/*.html routes.
- /writeups/ and /tryhackme/ list normalized content; /hackthebox/ has an honest empty state.
- _notes/, _research/, _projects/ and _topics/ are configured for real future material.
- The platform-neutral template is _templates/ctf-template.md.
- The [authoring workflow](docs/writeup-workflow.md) explains naming, metadata, assets and local checks.
- The immutable preservation baseline is docs/legacy-manifest.yml; do not replace original hashes with migrated hashes.

## Build and publication
_plugins/notebook.rb provides collection indexes, validation, title/TOC and keyboard-overflow helpers; legacy aliases are no longer needed.
The [Phase 3 report](docs/phase3-report.md) documents why retaining this small build-only plugin is recommended and what that means for a later hosting decision.
docs/, AGENTS.md, editor files, dependencies and build definitions are excluded from generated output.
No frontend JavaScript, trackers, remote fonts or external badge assets.

No deployment configuration, GitHub settings, commit or push was performed. [Phase 2 report](docs/phase2-report.md) remains historical evidence; its verification command delegates to the current complete-migration checks.
