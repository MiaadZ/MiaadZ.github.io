# Phase 6 — final QA and cleanup

## Result

Ready for normal ongoing publishing. The two approved h4cked repairs are local and await user review/publication. No commit, push, deployment, settings change, dependency installation, architectural redesign or workflow change was performed.

Direct production requests (not cached search results) verified all 36 HTML pages against a frozen local production build in UTC, matching hosted runner time-zone rendering. Structure, metadata, canonical routes, navigation, Featured/Latest order, topic membership and article content matched before the approved editorial repairs. All referenced production runtime assets matched local hashes. The newly exposed put.png screenshot also already exists live with its original hash. All 20 historical writeup routes resolve. Homepage, six topics, archives, TryHackMe, HackTheBox empty state, Tools and /404.html work; an intentionally nonexistent route returns HTTP 404 with the custom error page.

The sole default public profile link is https://tryhackme.com/p/S3Z4R. Its destination is correct; remote verification was rate-limited (HTTP 429), so its current profile response is not independently confirmed. No retry loop was used.

## Exact approved repairs

Only `_writeups/thm-h4cked.md` changed among content files:

1. `[10.10.10.10](10.10.10.10)` → `[10.10.10.10](http://10.10.10.10)`. Label and surrounding prose remain unchanged; the private lab address is deliberately not crawled by verification.
2. Added a blank line between the IP list item and the following bash fence, plus a blank line between its closing fence and the screenshot. The missing list/fence boundary had caused the screenshot and listener prose to become literal code. All nine screenshots now render; the PHP excerpt and listener command render in their intended blocks.

Every byte of source commands/output remains unchanged. Front matter, original date/title/tags/difficulty/OS/starred/source URL, credentials, flags, findings and screenshot files/hashes remain unchanged. The other 19 sources are untouched. Original Phase 1 manifest is unchanged. Exact approved text replacements live in `docs/editorial-corrections.json`; the preservation verifier applies these to the immutable baseline and still rejects any other body change. Former known-bug allowances were replaced by positive link/image/code checks. The optional rendered-baseline comparison accounts explicitly for the repaired malformed block and checks every other code block unchanged. Phase 4 verification recognizes only these exact corrections.

## Verification

Frozen production command:

```sh
TZ=UTC BUNDLE_FROZEN=true BUNDLE_PATH="$PWD/docs/vendor/bundle" JEKYLL_ENV=production PAGES_BASE_PATH='' bundle exec jekyll build --trace --destination _site --baseurl ""
```

Build passed without warnings/errors with the existing locked environment. `verify-writeups.py`, its Phase 2 compatibility entry point, `verify-phase4.py`, `verify-publication.py`, plugin Ruby syntax and `git diff --check` pass. The preservation check was additionally run against a saved live/pre-repair render: code/output/assets match except the exact approved h4cked rendering repair. All 20 legacy routes/metadata, screenshot hashes, six supported topic memberships/anchors and publishing exclusions pass.

Existing Chromium suite: 80 local viewport cases across desktop, 390px and 320px, plus six native 400% zoom cases (1280 → 320 CSS pixels, DPR 4, visual viewport scale 1) pass. An additional 27 live browser cases cover homepage, archives, topic, compatibility pages, Linux/Windows writeups and 404 at 1440/390/320px. No page-level horizontal overflow; all tested images load. Code/table regions remain keyboard-focusable and horizontally scrollable. First Tab exposes the skip link; Enter focuses main. TOC keyboard activation, visible focus, arrow-key code scrolling, reduced motion and decorative accessibility-tree exclusion pass. One H1/main and no skipped heading levels across all 36 local pages. Text-role contrast on both background/surface is at least 7.28:1; border contrast at least 3.59:1. No actual screen-reader test was performed. Initial desktop Chromium crashed; retry with the installed isolated headless browser completed all checks including real native zoom.

CSS remains 9,332 bytes (2,783 bytes gzip). No frontend JavaScript, external runtime assets or homepage images. No new visual assets or dependencies.

## Workflow QA — important distinction

[Latest run 41197389463](https://github.com/MiaadZ/MiaadZ.github.io/actions/runs/41197389463), commit `b8960b5c0d387717791a24baca749950e56cca26`: build, locked checks and SHA-pinned Pages artifact v5 upload succeeded without annotations. This was a manual validation-only run: configure-pages and deploy were skipped. It does not prove the publication path is warning-free.

[Last completed custom deployment 41196447246](https://github.com/MiaadZ/MiaadZ.github.io/actions/runs/41196447246), commit `34de025d2a59fbf606cc1c89b4f07774ef493944`: build and deployment succeeded. Its annotations include Node 20 metadata warnings for configure-pages and deploy-pages (and the since-replaced nested upload-artifact). The later cancelled push also confirms the configure-pages warning. The artifact warning is resolved; the two unchanged publication-only actions remain a maintenance item. They were not modified during this QA phase. Current SHA pinning, read-only build permissions, deployment-only Pages/OIDC writes and branch/event guards pass local policy checks.

## Authoring and hygiene

The approved template is unchanged. A future author creates `_writeups/<prefix>-<slug>.md`, fills factual normalized metadata including a unique explicit permalink, writes Markdown, and builds/publishes through the existing process. Homepage, Featured/Latest, archives, platform lists and existing topic/tag indexes update automatically. No manual index edit is needed. New topic definitions/mappings remain deliberate editorial work.

.obsidian/, _site/, vendor/, docs/vendor/ and .jekyll-cache/ are ignored and untracked. Development documentation, editor files, templates and workflow files are absent from generated output. QA browser profiles, screenshots and raw evidence remain only in ignored .jekyll-cache/. No useful documentation or original asset was removed. Isolated QA browser and preview server are stopped after verification.

Created: `docs/editorial-corrections.json`, `docs/phase6-report.md`.
Modified: `_writeups/thm-h4cked.md`, `docs/verify-writeups.py`, `docs/verify-phase4.py`, `docs/writeup-workflow.md`.
Moved/deleted: none. All other pre-existing project files remain unchanged.

## Remaining items

No additional functional site/content defect found. Publication-action Node runtime maintenance remains as described above; confirming the next actual deployment is warning-free requires a later user-authorized run. TryHackMe profile availability could not be confirmed because of HTTP 429. The corrected h4cked page is intentionally not yet live.

Optional future work, not defects: periodic local browser/screen-reader review, future factual Notes/Research/Projects, and deliberate topic curation as real content grows. No taxonomy expansion or speculative content was added.
