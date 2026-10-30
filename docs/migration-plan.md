# Preservation, migration and Phase 2 plan

Phase 1 specification, 2026-10-30. No theme removal, source moves, metadata migration, installation or redesign has happened.

## Baseline and confidence
legacy-manifest.yml inventories every current TryHackMe/*.md document: original metadata, whole-file SHA-256, body SHA-256, exact byte boundary, expected route, target path and local assets with hashes/dimensions.
Body means every byte after the complete closing YAML delimiter line and its newline; no newline normalization, whitespace cleanup or reserialization. Generator records body_offset_bytes so later tools hash the same slice. Preserve bodies byte-for-byte across platform/newline differences during relocation. A later reviewed metadata-reference normalization is the sole bounded exception described below.
The manifest also records every tracked file hash, allowing Phase 1 to prove no existing tracked file changed.
Only 20 writeups exist in this checkout. The expected ~30 must be reconciled before claiming the entire historical archive migrated.

## Current URLs
Source: _config.yml has baseurl empty, no global permalink override, no collections, no article permalink fields; the files are ordinary Jekyll pages.
Expected output: /TryHackMe/<exact original basename>.html.
This is source-derived Jekyll page behavior, NOT an observed generated/deployed route. Ruby exists but Jekyll is unavailable locally. No dependency installation or network verification was performed.
Jekyll build confirmation is mandatory before moving ANY source. If actual output differs, revise manifest routes and seek approval; do not silently apply inferred routes.

The manifest contains a full current route -> target source -> desired canonical route table. Target source:
_writeups/thm-<reviewed-slug>.md (flat; all 20 exact mappings are in the manifest).
Examples: AgentSudo.md -> thm-agent-sudo.md; h4cked.md -> thm-h4cked.md. HackTheBox convention is htb-<slug>.md; no unused platform prefixes or directories are predefined. Visible titles remain unchanged.
Desired canonical: identical to the confirmed current route, including /TryHackMe/, capitalization, punctuation, and .html.
Set explicit permalink per migrated document. Do not rely on collection :path or global pretty URLs to retain routes.
Do not create duplicate new canonical aliases under /writeups/ for legacy content. New writeups may use /writeups/<prefixed-source-stem>/ with explicit document permalinks.
URL generation uses relative_url for local links, absolute_url for canonical metadata. Avoid hard-coded deployment host strings.

## Compatibility concerns
- GitHub Pages paths are case-sensitive: Bruteit != bruteit, TryHackMe != tryhackme.
- Preserve assets/images paths and image bytes, including FTP.png case.
- Existing body fragments must survive Markdown engine/version changes; compare generated heading IDs and internal fragment targets.
- Root /tryhackme/, /hackthebox/ and /tools/ stay explicit.
- Raw /tools/#Nmap and current slugified #nmap links need a documented alias table. For old multiword IDs, retain compatible legacy targets only where valid and test encoded fragments; avoid introducing invalid IDs with spaces. Static compatibility may need reviewed constrained JS for otherwise unrepresentable historic fragments. Do not promise every fragment fixed by an HTTP redirect.
- Relative body links may resolve differently after collection moves; inspect actual rendered hrefs, not just Markdown filenames.
- site.pages will no longer contain migrated articles. During the pilot, use an explicit combined legacy-page + collection index, filtered before limit. Do not drop the 19 unmigrated pages.
- Adding type defaults must not classify root archive pages as writeups.
- Exactly one output document per legacy route; stale _site files must not conceal duplicate/missing results.
- Final metadata consumers use page.platform and page.source_url. Do not retain parent/link/machine_url as final interfaces. In a separately reviewed mechanical step, replace exact Liquid tokens page.parent -> page.platform, page.link -> page.source_url and page.machine_url -> page.source_url. Do not broadly replace these strings inside commands, quoted code or prose. Preserve surrounding Markdown, whitespace and heading text. Baseline hashes stay unchanged in the manifest; verify transformed bodies against baseline plus this exact allowlist and record new hashes separately. Remove legacy fields only after no consumer needs them.
- Archive filtering uses type and platform metadata, never platform folders or platform_slug.

## Existing bug worklist
1. machine_url/link: normalize link -> source_url and parent -> platform; fix exact Liquid metadata references to page.source_url/page.platform in the approved migration step. No permanent machine_url alias. No prose rewrite; verify only allowed token changes.
2. tag anchors: one slugify convention for badge links and canonical IDs; review legacy aliases and collisions.
3. recent entries: explicitly combine four editorial collections (plus temporary legacy pages); exclude ordinary pages/topics before sorting and limiting.
4. starred: absent means false; never partition lists into exact true and exact false groups.
5. difficulty: explicit mapping for known values; unknown omitted/neutral and reported, no generic red fallback. Difficulty is not severity.
6. empty archives: deliberate readable state, no fake content.
7. duplication: one archive layout and shared content-list include.
8. hidden titles: remove theme-wide suppression when local shell is ready; legacy bodies supply their own H1, new article layout supplies H1.
9. focus/motion: visible keyboard focus and reduced-motion rules; implement motion only after later approval.
10. authoring template: correct metadata contract; standardize new template and shared article layout on page.platform/page.source_url; preserve technical article prose.

## Reproducible build proposal (not installed)
After theme removal: Gemfile with a reviewed exact Jekyll version compatible with an agreed Ruby version; Jekyll's Kramdown/Rouge/Sass converter dependencies locked transitively. Pin Ruby through .ruby-version only after runtime selection. Commit Gemfile.lock only when dependency resolution is approved.
jekyll-sitemap can remain as the one explicit output plugin, pinned via lockfile. No jekyll-remote-theme, Minimal Mistakes, jekyll-include-cache, frontend package manager, JS bundler or arbitrary custom generator is needed for the target.
Do not invent lockfile/version compatibility now: exact versions and Pages deployment compatibility are unresolved. Existing Pages build mode must be confirmed before choosing standalone Jekyll vs github-pages dependency bundle.
Proposed local commands, only in an authorized later phase:
bundle install
bundle exec jekyll build --trace
Use frozen/locked resolution in repeatable verification once lockfile exists.
Do not change Pages settings or add Actions deployment in this phase. A custom-theme site can remain Jekyll; dependency/build mode is a separate approval.

## Phase 2: exact sequence and stop gates
1. Read AGENTS.md, verify branch/status and all manifest hashes. Resolve missing historical inventory or explicitly scope the migration to these 20.
2. Confirm build/deployment mode and approve exact Ruby/Jekyll dependency approach. If installation is necessary, request its explicit approval; do not run a package manager under Phase 1 authority.
3. Build the UNCHANGED theme site in an isolated development output location with production-equivalent config. Capture all generated article URLs, heading IDs, rendered links and warnings. Do not publish it.
4. Compare observed routes to manifest; review any differences. APPROVAL GATE: confirmed route map and per-file permalink strategy before ANY move.
5. Add publishing exclusions and development ignores without deleting local editor files; confirm docs/AGENTS/Obsidian do not appear in output.
6. Implement the five local layouts, minimal includes, CSS foundation and collection config. Keep theme available until its remaining responsibilities have replacements. Preserve Google verification. Remove runtime badges/profile shell from new presentation; retain article source.
7. Build temporary mixed-content indexes, keep legacy pages reachable. Scope unmigrated legacy layout: single to local article through configuration defaults, rather than introducing a sixth layout. Verify the remote single layout no longer controls legacy content before theme removal.
8. Pilot ONLY h4cked: move to _writeups/thm-h4cked.md, add explicit confirmed legacy permalink, article layout/legacy header flag and normalized factual metadata. First verify relocation body hash unchanged; then apply only separately reviewed exact Liquid metadata-token substitutions and verify that constrained diff. Preserve dates, tags, technical prose and screenshot bytes.
9. Test pilot at old URL, canonical URL, all nine images and existing fragments. Compare original relocation hash and expected token-normalized hash separately; validate rendered semantics, metadata and link targets. Test long code on UNMOVED Compiled, Windows metadata on Relevant and event/table structure on Advent of Cyber.
10. Remove theme dependency only after local shell/layouts/assets and remaining pages no longer need it. Build again and compare URL/link inventories. Report deliberate TOC behavior differences rather than silently claiming parity.
11. Verify Jekyll output, internal links/fragments, duplicate routes, preserved hashes and fields, no-JS navigation, keyboard focus, 320px/mobile/400% zoom and reduced motion. Run git diff --check. Report warnings and every created/modified/moved/deleted path.
12. STOP. APPROVAL GATE: review foundation + one migrated article before bulk migration, homepage rollout, taxonomy enrichment or motion. No commit/push/deploy.

## Later bulk migration
Only after pilot approval: move remaining 19 articles to the flat thm- filenames in the manifest, with explicit permalinks and allowed mechanical metadata/reference normalization. Verify one-to-one manifest mapping, exact unchanged body bytes outside the approved token allowlist, all asset bytes and protected metadata after each batch. Update archive consumers to collections, then retire temporary mixed index. Retain platform and Tools compatibility destinations. No invented summaries/topics/tools/techniques.
Separate reviewed work adds curated topics, new content, homepage copy and optional motion. Publication needs explicit approval.

## Phase 1 verification and limitations
Documentation and manifest generation require no package manager. Validate manifest metadata/hash coverage against all current articles, asset existence, uniqueness of route/target mappings and all original tracked-file hashes. Run git diff --check and list changes.
A Jekyll build is required by AGENTS before implementation completion; it is unavailable here and Phase 1 installs are prohibited. Report this limit openly: documentation completion does not assert build verification, rendered appearance, deployment routes or Phase 2 readiness.
