# Writeup authoring and local publishing workflow

Phase 3: all 20 existing writeups are normalized in the flat _writeups collection. Publishing here means preparing and verifying static output locally; committing and deploying remain user-controlled actions.

## Create real content
Copy _templates/ctf-template.md into _writeups/ with a clean lowercase kebab-case name.
- TryHackMe: thm-<slug>.md
- HackTheBox: htb-<slug>.md
- Define another platform prefix only when real content requires it.
No platform subdirectories. The visible title comes from title, never the filename.

The template is intentionally incomplete and is not publishable unchanged. Fill the real title, platform and ISO date; replace the commented permalink example with an explicit, unique route.
New-content example route pattern: /writeups/<prefixed-source-stem>/.
Existing migrated documents retain their exact /TryHackMe/<OriginalFilename>.html routes, including case. Never copy an existing article's permalink into a new one.

## Factual metadata
Use type: writeup, platform and source_url. parent/link/machine_url are obsolete and unsupported.
If a source URL is available, use the approved http/https source and link the platform through it. For an exercise without an external source, omit source_url; do not fabricate a URL.
OS and difficulty are optional if unknown. Remove unknown optional fields rather than inventing values; the layout handles absent or blank values.
Use the real original date; do not substitute Git timestamps or file modification dates.
Use tags: [] until factual tags are known and starred: false unless deliberately featuring the entry.
Optional summary/topics/techniques/tools/updated require reviewed facts. Topics must reference curated topic documents, not arbitrary tags. No automatic old-tag-to-topic conversion.

The new template opts into the native TOC with toc: true. Optional toc_label customizes its accessible disclosure label.
toc_sticky and toc_icon were theme-only settings and are no longer used.
The 20 preserved articles retain legacy_body_header: true because their protected bodies already contain H1 headings. Do not add this flag to a new template-based writeup: article.html supplies its title.

## Adapt the outline
The provided H2 sections are suggestions, not a checklist. Choose only sections supported by actual content:
- machine exercises: reconnaissance, access, escalation, findings and defensive notes;
- web labs: setup, hypothesis, testing and solution;
- DFIR: evidence, timeline, analysis and conclusions;
- CVE reproductions: versions, controlled setup, reproduction, observations and limitations;
- custom labs or challenges: objectives, method, evidence and outcome.
Keep technical commands/output accurate. Do not imply success, compromise, flags or conclusions without evidence.
No second body H1 is necessary. Template guidance is in Liquid comments and is excluded from rendered output.
The tag include is platform-neutral and generates local links without badge-service requests.

## Assets
Retain existing assets and their case-sensitive paths. New screenshots should use meaningful filenames and descriptive alt text under assets/images/.
Do not recompress, rename or edit existing screenshots as part of metadata/content organization work.
Preview images in context; a source reference can exist while Markdown accidentally renders it literally as code.

## Build and verify
Use Ruby 3.4.10, root Gemfile and Gemfile.lock. No new dependencies were introduced for Phase 3.
With the existing approved local bundle:
```sh
BUNDLE_FROZEN=true BUNDLE_PATH="$PWD/docs/vendor/bundle" bundle exec jekyll build --trace
python3 docs/verify-writeups.py _site
python3 docs/verify-phase2.py _site
git diff --check
```
If the root bundle was instead installed under vendor/bundle, use that BUNDLE_PATH. Follow AGENTS.md for dependency actions; new dependencies need approval.
Do not use docs/baseline.Gemfile for normal notebook builds; it retains historical theme dependencies.

verify-writeups.py verifies all 20 protected originals against the immutable Phase 1 manifest, allows only the three approved exact Liquid substitutions, checks YAML independently, validates local links/anchors/assets/canonical URLs and archive order, and reports inherited issues individually.
It also validates normalized names/schema for additional authored writeups. Its archive expectations include every actual collection writeup; it does not freeze the collection at 20 forever.
The older verify-phase2.py command remains as a compatibility entry point to the same current checks, not an assertion that the old mixed state still exists.
For a pre-existing render snapshot, add its directory as a second argument to compare all original rendered code blocks and asset references:
```sh
python3 docs/verify-writeups.py _site .jekyll-cache/phase3-baseline
```
That baseline directory is a local ignored artifact captured before Phase 3, not an additional published source.

For browser checks, serve _site on localhost and use an isolated Chromium profile/debug port; docs/verify-browser.py supports preview/debug origins as arguments and uses only Python's standard library. It writes ignored evidence under .jekyll-cache/phase3. It is a development tool, not frontend JavaScript.

## Review before any publication
Check the article, /writeups/, its platform view and /tools/ on desktop/mobile. Check keyboard focus, code/table scrolling, image legibility, headings and source links.
No analytics, comments, profile marketing or remote runtime assets.
The notebook plugin is build-only and currently required for complete output; see the Phase 3 report for the retention recommendation. Hosting/build-mode selection and deployment are separate decisions. This phase creates no workflow or hosting changes.

## Phase 4: curated topics and automatic discovery
The homepage, Latest, platform archives and Tools index update from published collection content; no manual article list is maintained in these templates.
Primary navigation always shows Writeups and Topics. Notes, Research and Projects appear automatically when they contain published material.

When a real article supports an existing knowledge route, add its reviewed slug to topics: []:
- web-security
- linux-privilege-escalation
- credential-attacks
- enumeration
- network-forensics
- reverse-engineering

Tags name lightweight descriptors/tools; topics express a curated relationship supported by the article. A tag is not sufficient evidence by itself.
Topic descriptions, selected starting points and featured-topic flags are intentionally editorial. Related lists and counts are automatic across all four content types.
docs/topic-evidence.json records the initial review of the protected 20 originals. Update that review record deliberately when reclassifying those originals. A new authored article with an existing topic slug requires no homepage/archive/platform-index edit.
Do not invent a topic to fill a gap. A new topic needs supported content, a real _topics page and a reviewed description.

Use these additional checks after building:
```sh
python3 docs/verify-phase4.py _site
```
This includes in-memory future-content fixtures only; no sample content is written.
docs/verify-browser.py now covers home/topics/identity, reduced motion and native Chrome 400% zoom when available, using an isolated local test profile. Its ignored output lives under .jekyll-cache/phase4/.
The existing writeup template remains unchanged.

Published discovery omits entries with published: false, future dates under normal Jekyll publishing rules, or status: draft. Direct draft-preview behavior is not a confidentiality mechanism.
