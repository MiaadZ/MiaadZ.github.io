# S3Z4R Security Notebook

A Markdown-first Jekyll security notebook. The local presentation foundation and one representative writeup migration are implemented; the remaining 19 writeups retain their original sources.

## Local build
Use Ruby 3.4.10 and the root Gemfile/Gemfile.lock. Jekyll 4.4.1 is the only direct target dependency. Dependency installation requires explicit approval under AGENTS.md.

With the already approved baseline installation:
```sh
BUNDLE_PATH="$PWD/docs/vendor/bundle" bundle exec jekyll build
python3 docs/verify-phase2.py _site
git diff --check
```

A fresh approved environment may install the root bundle into vendor/bundle. Do not use docs/baseline.Gemfile for the redesigned site's regular build; it preserves the historical theme build only.

## Source and publishing
- _writeups/ is flat; the pilot is thm-h4cked.md.
- Its explicit permalink preserves /TryHackMe/h4cked.html.
- TryHackMe/ contains 19 protected legacy sources.
- _notes/, _research/, _projects/ and _topics/ collections are configured; add real content only.
- _plugins/notebook.rb provides build-only compatibility, mixed indexes, contents and overflow helpers.
- docs/, AGENTS.md, editor files, dependencies and build definitions are excluded from generated output.
- No browser JavaScript, trackers, remote fonts or external badge assets.

Review actual hosting support for repository plugins before publishing. No GitHub settings or deployment workflow have been changed.

See [Phase 2 report](docs/phase2-report.md) for exact file accounting, verification and remaining review items. No bulk migration, commit, push or deployment has been performed.
