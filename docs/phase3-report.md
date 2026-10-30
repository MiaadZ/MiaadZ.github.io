# Phase 3: complete writeup migration and workflow

## Outcome
All 20 original writeups now reside in the flat _writeups collection. Nineteen sources moved in this phase; h4cked was already there and received the remaining approved Liquid field normalization.
No homepage redesign, Sass/CSS changes, motion, invented Notes/Research/Projects/Topics, dependency installation, commit, push, merge, deployment or GitHub configuration changes occurred.

The immutable docs/legacy-manifest.yml and historical Phase 2 evidence remain unchanged. See phase3-verification.json for per-article hashes, token counts, metadata status, confirmed routes and browser results.

## Complete mapping and URL preservation
Old source paths below are relative to TryHackMe/; final sources are relative to _writeups/. The URL column is BOTH the original public route and the final canonical/output route. Every row passed.

| Old source | Final source | Old public URL = new public URL | Result |
|---|---|---|---|
| Advent-of-Cyber-2025.md | thm-advent-of-cyber-2025.md | /TryHackMe/Advent-of-Cyber-2025.html | Preserved |
| AgentSudo.md | thm-agent-sudo.md | /TryHackMe/AgentSudo.html | Preserved |
| BasicPentesting.md | thm-basic-pentesting.md | /TryHackMe/BasicPentesting.html | Preserved |
| BrooklynNineNine.md | thm-brooklyn-nine-nine.md | /TryHackMe/BrooklynNineNine.html | Preserved |
| Bruteit.md | thm-brute-it.md | /TryHackMe/Bruteit.html | Preserved |
| Compiled.md | thm-compiled.md | /TryHackMe/Compiled.html | Preserved |
| Cyborg.md | thm-cyborg.md | /TryHackMe/Cyborg.html | Preserved |
| LazyAdmin.md | thm-lazy-admin.md | /TryHackMe/LazyAdmin.html | Preserved |
| MrRobotCTF.md | thm-mr-robot-ctf.md | /TryHackMe/MrRobotCTF.html | Preserved |
| Overpass.md | thm-overpass.md | /TryHackMe/Overpass.html | Preserved |
| Relevant.md | thm-relevant.md | /TryHackMe/Relevant.html | Preserved |
| RootMe.md | thm-root-me.md | /TryHackMe/RootMe.html | Preserved |
| Skynet.md | thm-skynet.md | /TryHackMe/Skynet.html | Preserved |
| Startup.md | thm-startup.md | /TryHackMe/Startup.html | Preserved |
| Tomghost.md | thm-tomghost.md | /TryHackMe/Tomghost.html | Preserved |
| TryHack3MBricksHeist.md | thm-tryhack3m-bricks-heist.md | /TryHackMe/TryHack3MBricksHeist.html | Preserved |
| h4cked.md | thm-h4cked.md | /TryHackMe/h4cked.html | Preserved |
| ignite.md | thm-ignite.md | /TryHackMe/ignite.html | Preserved |
| lookup.md | thm-lookup.md | /TryHackMe/lookup.html | Preserved |
| wonderland.md | thm-wonderland.md | /TryHackMe/wonderland.html | Preserved |

All output routes retain exact case and .html suffixes through explicit per-document permalinks. Filenames do not control titles or legacy public URLs. No platform source directories were created.

## Metadata and body preservation
All 20 titles, original dates, OS values, difficulties, tag arrays/order, starred states, platform facts and external source URLs independently match the original manifest.
Front matter now uses layout: article, type: writeup, platform and source_url; parent/link/machine_url are absent.
Retained toc and toc_label are used by the native contents disclosure. Removed toc_sticky/toc_icon only after confirming the local layouts/styles/plugin did not consume them.
legacy_body_header: true retains each protected source H1 while repositioning its identical rendered heading into the layout header.
No summaries, topics, techniques, tools or updated dates were added.

Exact byte comparison against the original Git objects permits ONLY:
- {{ page.machine_url }} -> {{ page.source_url }}
- {{ page.link }} -> {{ page.source_url }}
- {{ page.parent }} -> {{ page.platform }}

Across the original 20 bodies this totals 58 exact reference substitutions: 19 machine_url, 20 link and 19 parent. The h4cked machine_url correction had already happened in Phase 2; Phase 3 performs the other 57 substitutions.
Every other body byte is unchanged. This proves preservation of commands, output, flags, CTF credentials, findings, attack chains, explanations, dates and remediation outside the explicitly approved Liquid reference tokens.
All nine original screenshot files and source reference paths retain their hashes/bytes. All rendered code/command-output blocks and runtime asset references also match the fresh pre-migration Phase 2 build.

## Archives and compatibility
/writeups/ lists all 20 normalized collection documents, date descending with deterministic title/URL tie-breaks. Six entries remain featured. Listing metadata includes platform, OS, difficulty and date.
/tryhackme/ filters the same documents by platform metadata and lists 20; /hackthebox/ filters normalized metadata and presents "No entries published yet."
/tools/ remains the tag index, not a fabricated knowledge base. Its normalized tag anchors and valid case-sensitive single-word compatibility anchors resolve.
The homepage's mixed activity and featured selection continue to work through the existing notebook_entries interface. Its Markdown, layout and all stylesheet files are unchanged. Generated Home, Writeups, TryHackMe, HackTheBox and Tools HTML are also byte-identical to the pre-migration Phase 2 build.
In-memory rendering tests confirm article and listing templates omit both missing and blank optional metadata without empty fields/links.

## Template and authoring workflow
_templates/ctf-template.md is platform-neutral, with blank factual fields, explicit route guidance, optional H2 sections and hidden author guidance for machine exercises, web labs, CTF challenges, DFIR, CVE reproductions and custom environments.
The article layout owns new-document H1/metadata; the template does not add a duplicate H1 or profile block. It includes local tag links only when real tags exist.
docs/writeup-workflow.md documents source naming, immutable legacy URLs, factual schema, asset handling, template adaptation and local build/verification.
docs/verify-writeups.py is the current all-writeup preservation/schema/route/archive verifier. docs/verify-phase2.py remains a compatibility entry point to these current checks. It was also run in its original form before migration to verify the approved mixed baseline.
docs/verify-browser.py uses an isolated local Chromium debugging session and Python standard libraries. It adds no frontend JavaScript or dependencies.

## Build and tests
The pre-migration site built and its original Phase 2 verifier passed before any move.
A frozen-mode attempt exposed 35 blank CHECKSUMS entries in the root lockfile. Non-frozen Bundler did not persist them, so exact matching digests were copied from the approved baseline lock and checked against all 35 cached gem archives. No package declarations, versions, platforms or Bundler version changed.
The final full Jekyll 4.4.1 build succeeds with BUNDLE_FROZEN=true and no warnings. No installation, upgrade or network dependency resolution was needed.

Commands:
```sh
BUNDLE_FROZEN=true BUNDLE_PATH="$PWD/docs/vendor/bundle" bundle exec jekyll build --trace
python3 docs/verify-writeups.py _site .jekyll-cache/phase3-baseline
python3 docs/verify-phase2.py _site
ruby -c _plugins/notebook.rb
git diff --check
```

Checks passed:
- 20 original body byte comparisons and independent YAML metadata comparisons.
- All 20 exact original routes, canonical paths, source links and original heading anchors.
- All screenshot hashes and all rendered code/output and asset references.
- Newest-first archive order, featured count and platform compatibility archives.
- Local links/fragments, unique IDs, one H1/main per page, local runtime assets, publishing exclusions and no published source maps.
- No rendered heading-level jumps across the 20 articles.
- 44 Chromium views: every article at 320 CSS px; representative screenshot/code/Windows/Linux/table/raw-HTML/long-output pages and indexes at 390 and 1440 px; compatibility/index pages at 320 px.
- No page-level horizontal overflow; loaded images; keyboard-focusable code/table scroll regions.
- Keyboard skip link, native contents Space/Enter interaction, visible focus and ArrowRight horizontal code scrolling.
- Reduced-motion emulation; no optional motion implemented.

Browser screenshots and a fresh pre-migration build are ignored local artifacts under .jekyll-cache/phase3/ and .jekyll-cache/phase3-baseline/. The completed build is under ignored _site/.

## Exceptions requiring individual editorial review
1. h4cked: the pre-existing relative href="10.10.10.10" still resolves as a local relative URL. It was not rewritten.
2. h4cked: the put.png Markdown reference renders literally inside code in BOTH the pre-migration and final output. Eight screenshot images render; all nine source asset files/reference paths remain unchanged and valid. Fixing the existing Markdown structure is outside approved body normalization.
3. Existing raw inline styling remains protected, including colored prose in Compiled. Shared presentation focus/reflow tests pass, but this does not certify every historic inline color or screen-reader behavior.
4. Existing multiword raw tag fragments from the old index cannot all be represented as valid HTML IDs. Every currently emitted normalized tag link resolves; historical raw multiword fragment support remains a separate decision.
No metadata, date, technical-content, asset-hash or public-route preservation exception occurred.

Additional manual coverage remains: screen-reader review, other browser engines, actual desktop 400% zoom, and reading narrow screenshot text at full resolution. No image was recompressed.

## Plugin review and recommendation
Recommendation: B — retain the small build-only plugin. This is materially cleaner for the approved behavior; it adds no runtime assets or external dependencies.

Current responsibilities:
1. Gather only normalized writeups/notes/research/projects collections, sort by descending date and deterministic title/URL ties, expose notebook_entries.
2. Build a unique sorted tag index.
3. Fail builds for unsupported content types, missing title/date, colliding tag slugs, invalid archive collection selectors and duplicate output routes.
4. Extract/reposition the existing generated H1 without changing its source text, ID or link.
5. Validate source links using Ruby URI parsing and allow only http/https hosts without embedded userinfo.
6. Generate native details/summary TOC links from rendered H2–H4 IDs, respecting/escaping toc_label.
7. Wrap rendered code/tables in named, keyboard-focusable horizontal-scroll regions.

Removed as obsolete after normalization: the Phase 2 single-layout adapter, legacy site.pages aggregation and in-memory parent/link/machine_url aliases. This is migration cleanup, not a deployment compatibility redesign.

Standard Jekyll/Liquid can reasonably handle collection concatenation, basic sorting, tag loops and metadata filtering. It cannot provide the complete current validation/error behavior or robust URI checks directly, and replacing the title/TOC/overflow helpers would require brittle HTML string parsing, more Liquid code, altered authoring contracts or additional dependencies. Removing it now would not be a trivial behavior-preserving change.
The helpers operate on Jekyll-generated HTML, not arbitrary external HTML; the current heading/HTML assumptions are documented and preservation/browser checks cover the actual content.

Publication implications: the current site requires a normal non-safe Jekyll build that loads repository plugins. A future custom GitHub Actions build could retain this implementation. A standard safe-mode GitHub Pages build would require a separate tested port of plugin behavior to supported Liquid/build checks before publication. Neither route is configured or selected here.

## Project file accounting
Created:
- docs/verify-writeups.py
- docs/verify-browser.py
- docs/writeup-workflow.md
- docs/phase3-verification.json
- docs/phase3-report.md

Modified:
- Gemfile.lock (35 verified checksum completions only)
- README.md
- _includes/content-list.html
- _includes/ctf-badges.html
- _layouts/article.html
- _plugins/notebook.rb
- _templates/ctf-template.md
- _writeups/thm-h4cked.md
- docs/verify-phase2.py

Moved: the 19 source mappings in the table, excluding h4cked (already moved in Phase 2).
Deleted: no standalone source/assets/docs. Old paths disappear as part of the approved moves. No screenshots were changed.
Ignored artifacts: _site/, .jekyll-cache/phase3-baseline/, .jekyll-cache/phase3/ browser profile/screenshots/evidence. These are local verification output, not published project content.

## Proposed Phase 4 scope — not started
Review the two inherited h4cked content issues and authorize any narrowly scoped correction separately.
Approve final homepage technical narrative and reviewed topic routes backed by real content; do not manufacture Notes/Research/Projects to fill sections.
Choose the publication/build approach after reviewing the plugin recommendation, without deploying automatically.
Complete manual accessibility/browser checks. Optional motion remains a separately approved enhancement.
No Phase 4 work has begun.
