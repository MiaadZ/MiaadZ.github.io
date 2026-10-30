# S3Z4R Security Notebook: architecture specification

Phase 1 specification, 2026-10-30. This document authorizes no implementation.
Read alongside content-schema.md, design-system.md, migration-plan.md and legacy-manifest.yml.

## Product and scope
A technical security portfolio and personal knowledge base: approximately 70–80% technical publication, 20–30% terminal identity. No résumé, employer/university biography, recruiting funnel, fake terminal or generic Articles collection.

## Target tree
Only create collection folders when they contain real material; no placeholder .gitkeep files or invented content. The writeups collection is flat: no platform subdirectories. Source prefixes thm- and htb- prevent collisions; define other prefixes only when real content requires them. Source filenames never determine visible titles.

```text
_config.yml
Gemfile
Gemfile.lock
.gitignore
_data/navigation.yml
_layouts/
  default.html
  home.html
  article.html
  archive.html
  topic.html
_includes/
  head.html
  header.html
  footer.html
  content-list.html
  ctf-badges.html
_sass/
  _tokens.scss
  _base.scss
  _shell.scss
  _components.scss
  _article.scss
assets/
  css/main.scss
  images/                    # existing assets retained at current paths
_writeups/
  thm-agent-sudo.md
  thm-basic-pentesting.md
  thm-h4cked.md
  thm-lookup.md
  ...                        # remaining current writeups; see manifest
_notes/
_research/
_projects/
_topics/
_templates/
  ctf-template.md
docs/
  architecture.md
  content-schema.md
  design-system.md
  migration-plan.md
  legacy-manifest.yml
index.md
writeups.md
notes.md
research.md
projects.md
topics.md
tryhackme.md                  # legacy platform archive
hackthebox.md                 # legacy platform archive
tools.md                      # legacy tag/fragment compatibility
404.html
README.md
AGENTS.md
```

Existing files not represented as future presentation components are not automatically authorized for deletion. Keep assets/images/profile.png as source material even after removing its public sidebar. Retire _includes/head/custom.html only after its verification metadata is transferred and callers checked. Do not create JavaScript until a concrete enhancement needs it.

## Collections and routes
Configure writeups, notes, research, projects and topics with output: true.
For NEW content, use explicit document permalinks:
- writeup: /writeups/<source-stem>/
- note: /notes/<slug>/
- research: /research/<slug>/
- project: /projects/<slug>/
- topic: /topics/<slug>/

Collection fallback patterns may use /writeups/:path/, /notes/:path/, etc.; explicit document permalinks are authoritative and keep source filenames and public routes independent. Legacy writeups retain their old .html routes, not the new-content pattern.

The new-content route proposal uses the prefixed source stem for uniqueness (e.g. /writeups/thm-agent-sudo/); explicit permalinks remain authoritative. No current legacy route is changed by this proposal.

Platform is metadata, never inferred from a folder. Select documents by type and platform. Navigation is Home (brand), Writeups, Notes, Research, Projects, Topics. Existing platform archives remain compatibility destinations.

## Five layouts: inheritance and real uses
- default: root layout; document language, head include, skip link, header/nav, one main landmark, footer and local assets.
- home -> default: index only; landing hierarchy below.
- article -> default: every writeup, note, research document and project; conditional metadata by type, readable body and topic links. For writeups render platform · OS · difficulty · date, omitting absent values and separators; link platform to validated page.source_url when present. No platform-specific hard-coding.
- archive -> default: four type archives, Topics index and filtered platform archives. No separate platform layout.
- topic -> default: curated introduction and four grouped content lists.

Use layout front matter for inheritance. Only default owns html/body/main; nested layouts must not duplicate landmarks. No single/writeup/note/research/project layouts.

Legacy bodies already contain H1 and badge includes. article supports legacy_body_header: true: do not add another H1 or duplicate full metadata block; retain body heading and its anchors. Final body metadata references use page.platform and page.source_url; legacy field references require a narrowly reviewed mechanical token migration, never prose rewriting. New documents have no body H1 and use the layout heading. A build-time, server-rendered TOC is deferred until a concrete compatible implementation is selected; do not introduce heading parsing JavaScript just to replace theme TOC.

## Includes: smallest useful set
- head.html: escaped titles/descriptions, canonical URL, local CSS, Google verification; no runtime remote assets.
- header.html: brand and navigation, current-page state; standard links, no fake shell.
- footer.html: short notebook identity, restrained TryHackMe link.
- content-list.html: receives an already selected/sorted entries array and heading level; loops cards/list rows and handles empty state. Shared across home, archives and topic groups.
- ctf-badges.html: existing body-call compatibility; semantic text badges with normalized links. Retain its filename to protect bodies.

Do not split each badge, icon, breadcrumb or list row into another include without repeated real use.

## Homepage contract
1. S3Z4R / Security Notebook hero; optional short decorative prompt.
2. Concise reviewed technical philosophy and generalized progression: software -> backend/Linux -> SOC/security operations -> offensive/security engineering. No inferred biography or detailed timeline.
3. Up to three starred entries across the four editorial collections. Hide the section if none; show existing titles/metadata when summaries are absent.
4. Latest six entries across writeups + notes + research + projects, each with WRITEUP/NOTE/RESEARCH/PROJECT text label.
5. Selected curated topics with reviewed descriptions. Omit this section until topics exist.
6. Restrained TryHackMe identity link, not a social/contact panel.

Concatenate the four collection arrays explicitly; exclude topics and ordinary pages. Select eligible content before sort and limit. Date descending; ties use title then URL in deterministic order. Use original date, not Git time or updated, for latest activity.

## Archive behavior
Page metadata: archive_collection selects one allowed collection; optional archive_platform selects exact platform metadata value. Validate these values; unknown selectors are errors, not empty archives.
For example writeups.md: archive_collection: writeups; tryhackme.md additionally archive_platform: TryHackMe.
Sort date descending, then title and URL for ties. Featured status is a badge, not an implicit reorder. Optional year headings preserve the same order.
Entries show type, title, date and available summary; writeups additionally show platform, OS and difficulty when known. Never output dangling separators or placeholder facts.
Known empty archives show a heading and honest "No entries published yet." Unknown metadata values must be reported separately.
No pagination or filtering JavaScript initially; all entries remain usable without JS. Topics index lists real topic documents alphabetically.

## Topics
Each _topics document owns a unique stable slug, title, reviewed introduction and optional featured flag. Editorial documents link through topics: [slug]. Resolve exact slugs, validate unknown references and duplicate slugs, then group by type. Show only populated groups; a topic with no linked content must have an intentional reviewed purpose before publication.
No automatic old-tag-to-topic conversion. Existing tags are evidence for review, not authoritative taxonomy. Tools/technology tags do not prove techniques. Topic pages are knowledge routes, not invented tutorials.

## Privacy and publishing contract
Remove public GitHub identity link, location and author/profile sidebar from the new shell; keep TryHackMe. Preserve article source citations and existing attribution. Keep Google site verification currently in _includes/head/custom.html; it is public verification metadata, not analytics.
No trackers, analytics, comments, auth, cookies or third-party JS. Replace Shields.io images with local HTML/CSS text. Use system fonts and local assets.
Explicitly exclude docs/, AGENTS.md, README.md, Gemfile, Gemfile.lock and development-support files from Jekyll output where appropriate. Explicitly exclude .obsidian/, even though dot directories are normally ignored; do not force-include it. Never blanket-include dotfiles.
.obsidian workspace records local/editor history and its 2.3 MB theme is unrelated to site styling. Leave these existing untracked files alone; propose .gitignore entries later. Do not assume .gitignore controls Jekyll publication.
Phase 1 docs are temporarily ordinary source files: docs has no leading underscore and Jekyll can copy Markdown without front matter as static files. Do not deploy this branch before output exclusions are implemented. No config change is made in this phase.
Canonical base is the configured site URL plus absolute page URL. Escape text/attributes and serialize JSON with proper filters; validate optional external URL schemes. No blanket target=_blank requirement. Where used, add rel=noopener noreferrer.
Host-supported security headers require a separate hosting decision; meta CSP cannot implement every response header. Do not claim headers are applied by a GitHub Pages repository file.
