# Phase 2 foundation and pilot report

Completed locally on 2026-10-30. No commit, push, merge, deployment, GitHub settings change or bulk migration. The original preservation manifest remains unchanged.

## Result
Five repository-owned layouts, five active includes, five Sass partials, local stylesheet, content-type navigation, shared article presentation, mixed legacy/collection archives and explicit publishing exclusions are implemented.
Only h4cked migrated:
- old source: TryHackMe/h4cked.md
- new source: _writeups/thm-h4cked.md
- canonical/output route: /TryHackMe/h4cked.html
- unchanged source URL: https://tryhackme.com/room/h4cked

The 19 remaining writeups are byte-for-byte identical to Phase 1. No optional summary/topics/techniques/tools were invented. Empty content-type archives contain honest empty states, not fabricated entries.

## Build and dependency evidence
Jekyll 4.4.1 and Ruby 3.4.10; root Gemfile.lock resolved offline using already installed gems. No dependency installation occurred during this resumption. Target Gemfile has only Jekyll as a direct dependency; all transitive versions are locked for x86_64-linux-gnu.
Existing approved installation lives under docs/vendor/bundle because Bundler resolved the relative path against docs/baseline.Gemfile.
Build command used:
```sh
BUNDLE_PATH="$PWD/docs/vendor/bundle" bundle exec jekyll build --destination /tmp/s3z4r-phase2-site --trace
python3 docs/verify-phase2.py /tmp/s3z4r-phase2-site
git diff --check
```
For an approved fresh installation, use the root Gemfile; no reinstall is needed here.

Baseline first attempt failed because Jekyll scanned docs/vendor/bundle and encountered Jekyll's ERB example post with an unevaluated date. No source content error caused this.
Successful baseline used an isolated copy of the 40 original tracked files, original configuration plus a build-only plugin override explicitly loading jekyll-remote-theme/include-cache/sitemap. It fetched Minimal Mistakes 4.27.3, preserved original content and confirmed all 20 .html routes. Theme Sass emitted import/global-function/color/division deprecation warnings (235 repetitive warnings suppressed). These are baseline warnings.
The final target build succeeds without warnings and without remote theme fetches. Target output: 30 HTML pages and approximately 6 KB compressed local CSS; source maps excluded. Build timestamps/cache behavior are not asserted bit-for-bit reproducible; dependency versions and source inputs are pinned.

## Minimal Mistakes and compatibility
No active theme configuration, theme layouts/assets, Shields.io, external scripts/fonts or profile sidebar remain in the target build.
Historical references and baseline-only dependencies remain in docs and ignored installed dependencies; docs/baseline.Gemfile and its installer-generated lockfile intentionally preserve baseline reproducibility.
_includes/head/custom.html is retained as a retired, inert hook; verification moved to head.html.

A concrete implementation constraint required _plugins/notebook.rb: explicit layout: single in 19 protected legacy front matters overrides configuration defaults. The adapter maps their layout and normalized metadata IN MEMORY; no sixth layout or source modification.
It also supplies temporary source-url aliases for old heading/body references. The normalized layout uses page.platform/page.source_url, never page.machine_url. The pilot keeps its original page.parent/page.link BODY tokens unchanged; only its machine_url token changed as authorized. Parent/link compatibility values are supplied in memory, not retained in pilot front matter.
The adapter builds deterministic mixed listings, validates duplicate routes/tag-slug collisions/archive collection selectors, supplies a server-rendered contents disclosure and keyboard-scrollable code/table wrappers.
Existing generated H1 is repositioned into the article header without changing its ID/text/link or source bytes.
This requires a normal Jekyll build with repository plugins enabled. Safe-mode/native hosting compatibility is not established; review actual GitHub Pages build mode before any publication. No hosting settings were changed.

## Preservation evidence
- Original pilot body SHA-256: 0794f828785ffb3c5a51f5e386d5b2941fc8ce8596e08d50441acd0817ed50ed
- Migrated body SHA-256: 3a086ada62fe147323a657d3c90db4f0207e75e29527c6f63f6c4f81489709e0
- Exact comparison passes after ONE substitution: {{ page.machine_url }} -> {{ page.source_url }}.
- Therefore all commands, flags, credentials, findings, attack chains, remediation and prose outside that exact token are unchanged.
- Independent YAML comparison passes for title, date, platform, OS, difficulty, tags, starred, source URL and explicit permalink.
- All nine screenshot hashes match original manifest.
- Remaining 19 whole-file hashes match original manifest.
- All 20 public routes build; all original article heading anchors survive.
- Root writeup archive lists 20 entries including the one collection document.
- docs/phase2-verification.json records baseline routes/heading IDs and browser evidence; no writeup prose or credentials are copied into it.

## Verification and accessibility
Repeatable standard-library preservation/link checks are in docs/verify-phase2.py.
Generated output passes unique ID, one-H1/one-main, internal link/fragment, local runtime asset and publishing-exclusion checks, with one explicitly identified pre-existing content link below.
Headless Chromium inspected home, writeups, h4cked, Compiled, Relevant, Advent of Cyber, Tools and Notes at 1440, 390 and 320 CSS px: 24 views, no page-level horizontal overflow, images loaded, one H1 each and no external runtime assets.
Keyboard: first Tab reaches skip link; Enter moves focus to main; Space opens and Enter closes native contents; visible solid focus outline. Reduced-motion media emulation succeeds; no animations or frontend JavaScript are implemented.
Shared text/accent tokens pass 4.5:1 on background/surface; border and focus meet 3:1. Border token increased to #657489 after testing.
Screenshot previews were visually inspected on desktop/mobile; temporary files are /tmp/s3z4r-home-{1440,390}.png and /tmp/s3z4r-h4cked-{1440,390}.png.

## Remaining manual review and work
- h4cked contains a pre-existing relative href="10.10.10.10"; it is also present in baseline output and intentionally not rewritten.
- Existing inline colors and heading-level irregularities in legacy bodies remain protected; shared theme checks are not a full accessibility audit of historical content.
- Full screen-reader review, additional browser engines and actual 400% browser zoom remain manual checks. The 320 CSS px reflow check passes.
- Some screenshot text is intrinsically small at mobile width; original asset bytes/paths are retained, not recompressed.
- Original in-body metadata blockquotes remain alongside normalized header metadata because removing them would change protected bodies.
- TOC is native details/summary; theme-specific sticky/icon presentation is not reproduced.
- Tools retains normalized anchors and valid case-sensitive single-word legacy aliases. Old multiword raw IDs cannot all be represented as valid HTML IDs; manual fragment compatibility review remains.
- Root target lockfile currently covers Linux; other build platforms need deliberate local resolution, not an unreviewed install.
- No sitemap plugin in the minimal target Gemfile; sitemap generation can be explicitly reviewed later.
- Final homepage narrative, selected curated topics, optional motion and remaining migration are later phases. No fake projects, research or notes were created.
- Actual hosting/build mode remains unverified. Do not deploy until its plugin support is reviewed.
- Archive scope remains the 20 available writeups; the approximate larger historical inventory is unresolved.

## File accounting (cumulative Phase 2)
Created:
- .ruby-version (before dependency gate)
- Gemfile (before dependency gate)
- docs/baseline.Gemfile (before dependency gate)
- .gitignore
- Gemfile.lock
- 404.html
- _layouts/default.html
- _layouts/home.html
- _layouts/article.html
- _layouts/archive.html
- _layouts/topic.html
- _includes/head.html
- _includes/header.html
- _includes/footer.html
- _includes/content-list.html
- _plugins/notebook.rb
- _sass/_tokens.scss
- _sass/_base.scss
- _sass/_shell.scss
- _sass/_components.scss
- _sass/_article.scss
- assets/css/main.scss
- writeups.md
- notes.md
- research.md
- projects.md
- topics.md
- docs/verify-phase2.py
- docs/phase2-verification.json
- docs/phase2-report.md

Modified:
- _config.yml
- _data/navigation.yml
- _includes/ctf-badges.html
- _includes/head/custom.html
- _templates/ctf-template.md
- index.md
- tryhackme.md
- hackthebox.md
- tools.md
- README.md

Moved:
- TryHackMe/h4cked.md -> _writeups/thm-h4cked.md (front matter normalized; exact one-token body repair)

Deleted: no standalone files. Git's unstaged status shows the move as old-path deletion plus new untracked path until staged.
docs/baseline.Gemfile.lock and docs/vendor/bundle were produced by the user's approved dependency installation, not by the foundation source edit.
AGENTS.md and original Phase 1 docs/manifest were already present and remain unchanged.
