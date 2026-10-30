# Content schema specification

Phase 1 only. No existing front matter or prose is changed.

## Shared editorial fields
Required: title (nonempty string), type (writeup|note|research|project), date (ISO YYYY-MM-DD), permalink (absolute site path).
Optional: summary (reviewed factual string), updated (date of substantive content revision), tags, topics, techniques, tools (arrays of strings), starred (boolean, absent means false).
Date is original editorial metadata, never silently replaced with commit/build time. Existing date values remain exact. Unknown facts remain absent; do not fill summaries from assumptions.
Collection-scoped defaults provide layout: article and matching type. Explicit type may be retained for author clarity; validation rejects collection/type mismatch. Do not use custom type as a substitute for collection membership.
Layout is presentation metadata, not a content taxonomy. Legacy-only legacy_body_header is a boolean presentation compatibility flag.

## Taxonomy responsibilities
- platform: lab/content provider display name, e.g. TryHackMe or HackTheBox. Used directly for metadata filtering/grouping, not inferred from filenames. No platform_slug field is required.
- tags: lightweight discovery labels; existing mixed tags retained verbatim during mechanical migration.
- topics: curated knowledge-route slugs matching real _topics documents. Explicit editorial relationship, not inferred from tag presence.
- techniques: methods actually demonstrated, e.g. traffic-analysis; reviewed controlled slugs.
- tools: software actually used; reviewed tool identifiers/labels. Do not automatically move every old tag here.
New labels should use consistent identifiers, with human-readable presentation where needed. Alias mappings for old tags are explicit and collision-checked. Do not lowercase or rewrite old arrays as part of source relocation.

## Writeups
Shared fields plus platform. The normalized writeup interface is page.platform and page.source_url.
source_url is an approved absolute http/https URL when a source exists; omit it for environments without an approved external source. os and difficulty are factual metadata when known; preserve all current values. Difficulty supports Easy|Medium|Hard|Insane; unknown values require review, not a red fallback.
parent -> platform and link -> source_url are mechanical field migrations. parent, link and machine_url are not final interfaces. Do not add machine_url as a permanent alias.

Final normalized example:

```yaml
title: "Agent Sudo"
type: writeup
platform: TryHackMe
source_url: "https://tryhackme.com/room/agentsudoctf"
os: Linux
difficulty: Easy
date: 2025-11-08
tags: [FTP, Binwalk, Hydra, SSH]
starred: false
```

Per-document permalink is additional routing metadata, required to preserve legacy URLs; e.g. /TryHackMe/AgentSudo.html for this article. Presentation flags such as legacy_body_header are separate from factual content.
Optional reviewed enrichment: summary, topics, techniques, tools, updated. Do not invent values.

The collection is flat. TryHackMe source filenames use thm-<slug>.md; HackTheBox uses htb-<slug>.md. Define no unused future-platform prefixes. The visible title comes from title, not the source stem. Exact mappings for all 20 existing files are recorded in legacy-manifest.yml.

A later approved migration must mechanically replace only exact Liquid references: page.parent -> page.platform; page.link -> page.source_url; page.machine_url -> page.source_url. Includes/templates also adopt normalized fields. This is a bounded metadata-reference repair, not permission to edit technical prose, code, flags, dates or findings. Phase 1 performs no such replacements in existing articles.

## Notes
type: note; optional environment (string), prerequisites (array of strings), status (draft|published|archived). A concise task/reference scope is preferable to forced long-form headings. Published is the effective default. Draft handling is a build/publication rule, not confidentiality.

## Research
type: research; optional status (draft|published|archived), environment, references (array of title/url objects), vulnerability_ids (reviewed identifiers).
Use content for research question, method, findings and limitations; no required invented results, CVEs or disclosure claims. Deeper technical articles belong here; no Articles collection.

## Projects
type: project; optional status (active|maintenance|archived), repository_url, demo_url (http/https), license, version.
Only real authored/maintained work. Project source links are distinct from exposing a personal GitHub identity panel; public project links need editorial approval. Do not invent repositories or demos.

## Topics
Required title, slug, permalink. Default layout: topic. Optional featured boolean.
Introduction is Markdown body. Editorial relations come from document topics arrays, not repeated manual lists in both directions. Topics do not appear in recent editorial activity and do not require fictional publication dates.

## Compatibility and validation
Existing layout: single becomes article only during approved migration. Preserve toc fields in source during mechanical migration; unsupported theme settings must not be mistaken for implemented behavior.
Default starred false must work in selectors as well as rendering: use a single list and conditional badge, not true/false partitions.
Validate dates, duplicate output routes, required values, taxonomy references and external URL schemes. Strict Liquid variables cannot be enabled blindly while optional fields are unguarded. Missing optional metadata yields omission, not blank badges.
All 20 original body hashes and asset hashes remain the immutable baseline. Source relocation alone must preserve body bytes. A separately reviewed exact Liquid-reference replacement necessarily changes body hashes: verify the result against the baseline with ONLY the approved token substitutions applied, and record post-migration hashes separately. Preserve all remaining body bytes and every asset byte. Front-matter changes require a field allowlist and original metadata comparison; dates/tags/OS/difficulty/starred/source facts remain unchanged.
