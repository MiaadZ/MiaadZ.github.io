# Phase 7 — publishing workflow and content expansion

## Outcome

Ready for routine publishing. No new article, note, research entry, project or topic was published or retained as test content. Existing homepage, architecture, layouts, visual identity, writeups, topic descriptions/mappings and public routes are unchanged. No dependencies added/installed, commit, push, deployment or GitHub setting change.

Created three unpublished authoring templates: `_templates/note-template.md`, `_templates/research-template.md`, `_templates/project-template.md`. Each uses matching normalized type, title/date, optional summary/tags/topics, and `published: false` until reviewed. Research supports optional status/references; projects support optional status and real public repository/demo URLs. Section outlines are adaptable Liquid-comment guidance. The existing writeup template is unchanged.

## Authoring

README now gives the directory map, template/copy/fill/write/build/validate process, local commands and actual Actions publication behavior. `docs/writeup-workflow.md` is the concise ongoing guide rather than a sequence of historical phase notes. It distinguishes WRITEUP/NOTE/RESEARCH/PROJECT, factual metadata, prefix naming, stable URLs, publication controls and topic curation.

Writeups remain flat: `thm-<slug>.md` for TryHackMe, `htb-<slug>.md` for HackTheBox. No unused abbreviations predefined. Display title/platform come from metadata. Notes/research/projects use `<slug>.md` in their collections. Fill a unique explicit permalink; never reuse or change an existing legacy route. Build/review then user-controlled commit/push are the only publishing steps; homepage, activity, archives, platform views and existing topic/tag lists update automatically.

Existing topics use supported slugs in `topics: [...]`. Tags do not automatically become topics. New curated routes require meaningful scope, real supporting content, a human-readable description and deliberate mappings. A new topic page is discovered without manual index changes. The historical evidence record continues protecting the original 20 mappings, rather than becoming a manual registry of every future article.

## Real friction corrected

- Writeup archive verification previously expected drafts/future sources in published lists; expectations now follow normal production publication rules.
- The HTB verifier assumed the collection must stay empty; it now checks metadata-driven entries and requires an empty state only when none exist.
- Topic verification assumed the initial topic count was permanent and always used plural counts; it now checks actual published topic documents, including singular counts, while retaining original reviewed membership/evidence safeguards.
- The Phase 4 fixture runner overrode an explicitly selected bundle path; it now honors the existing environment, allowing isolated builds without reinstalling gems.
- Generic plugin validation now checks normalized metadata across all four published types: string title/summary, type agreement, original date presence, local explicit permalink, array fields, boolean starred and safe HTTP(S) source/project/reference shapes. Required date checking happens before Jekyll's publisher can silently supply build time for a missing date. No article presentation behavior changed.

## Isolated new-content proof

`docs/verify-authoring.rb` uses existing Jekyll/Ruby libraries and creates a disposable source under ignored `.jekyll-cache/phase7/`. It copies build sources, fills all four actual templates with clearly labeled test metadata, builds them through article.html and checks:

- all four routes render with one H1 and the shared article shell;
- automatic own-archive, mixed Latest, conditional navigation, existing-topic membership and backlinks;
- first HTB writeup discovery without platform-index edits;
- intentional new-topic discovery and correct one-entry count, without real taxonomy changes;
- eight draft/future fixtures produce no output or discovery entries;
- actual preservation/link/archive/Phase 4 verifiers pass against the augmented build;
- 14 invalid metadata mutations are rejected, plus a real source-file build missing its original date fails;
- no template output and no retained fixture source or generated fixture site.

All checks pass. The disposable source/output is removed in ensure, even on failure. Only ignored numeric evidence remains. The normal source still contains the same 20 writeups, six topics and no Notes/Research/Projects documents.

## Actions maintenance

Only two workflow references/comments changed:

| Action | Old | Prepared stable Node 24 pin |
| --- | --- | --- |
| configure-pages | v5 / `983d7736d9b0ae728b81ab479565c72886d7745b` | v6.0.0 / `45bfe0192ca1faeb007ade9deae92b16b8254a0d` |
| deploy-pages | v4 / `d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e` | v5.0.1 / `368f82528645a54fb793d4d04e342629a3f51346` |

Official latest stable release tags were resolved to these commits and pinned action.yml files reviewed: both declare `runs.using: node24`; existing inputs/output names and permissions remain compatible. All unchanged JavaScript actions and the nested upload-artifact also declare node24. Exact text comparison against HEAD confirms no workflow changes beyond these two references: triggers, permissions, guards, environment, concurrency, checkout, Ruby/Bundler/Jekyll, build commands and deployment wiring remain intact. Deploy v5.0.1 includes upstream polling backoff/jitter; no custom/local deployment logic was changed.

Publication runbook pin table is current. Official sources: [configure-pages v6.0.0](https://github.com/actions/configure-pages/releases/tag/v6.0.0), [deploy-pages v5.0.1](https://github.com/actions/deploy-pages/releases/tag/v5.0.1).

The prepared updates have not run on GitHub in Phase 7. Known Node 20 declarations are addressed locally; warning-free hosted publication must be confirmed after a later user-controlled commit/push/deployment. No claim that a new hosted run occurred.

## Final verification

Frozen production Jekyll build with UTC, existing root Gemfile/lock, existing repository-local gems: PASS, no warnings/errors. `verify-writeups.py`, Phase 2 compatibility wrapper, `verify-phase4.py`, `verify-publication.py`, `verify-authoring.rb`, Ruby syntax and `git diff --check`: PASS. YAML parses and least-privilege policy is intact. All 36 normal HTML pages, 20 original URLs/bodies/metadata and screenshot hashes preserved. No templates, docs or fixture artifacts emitted. No browser rerun: presentation sources are unchanged; Phase 6 browser evidence remains applicable.

## Files

Created:
- `_templates/note-template.md`
- `_templates/research-template.md`
- `_templates/project-template.md`
- `docs/verify-authoring.rb`
- `docs/phase7-report.md`

Modified:
- `.github/workflows/pages.yml`
- `README.md`
- `_plugins/notebook.rb`
- `docs/publication.md`
- `docs/verify-phase4.py`
- `docs/verify-writeups.py`
- `docs/writeup-workflow.md`

Moved/deleted project files: none. Temporary test sources/output were removed. Existing writeup/template/layout/topic/configuration/dependency files remain unchanged. Remaining external verification: the next actual hosted run of the new action pins, controlled by the user.
