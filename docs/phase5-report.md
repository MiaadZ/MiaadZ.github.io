# Phase 5 report

Prepared local custom GitHub Actions publication; no external publication or settings changes.

Created `.github/workflows/pages.yml`, `docs/verify-publication.py`, `docs/publication.md`, and this report. No existing project file modified, moved or deleted by Phase 5. Existing uncommitted Phase 4 work remains intact. Temporary ignored `_site` and `.jekyll-cache/phase5-entry.json` are local verification artifacts.

Triggers: PRs targeting `main`, pushes to `main`, manual dispatch. Deployment requires `refs/heads/main` and either push or explicit manual `deploy: true`; PR/manual-default builds cannot deploy. `main` comes from local origin/HEAD; confirm remotely during manual launch preparation.

All five actions are SHA-pinned; exact refs, permissions and supply-chain rationale are in [publication.md](publication.md). Build permissions are read-only contents/Pages; deploy alone gets Pages write and OIDC write. Credentials are not persisted. No new dependencies installed or introduced.

Local validation: frozen production build succeeded without warnings/errors using Ruby 3.4.10, Bundler 4.0.3, Jekyll 4.4.1. Command: `bundle exec jekyll build --trace --destination _site --baseurl "$PAGES_BASE_PATH"` with production/frozen environment and empty root base path; destination `_site`. Plugin executes normally. YAML and security policy checks, plugin Ruby syntax, writeup verifier, Phase 4 verifier and `git diff --check` pass. All 36 HTML pages checked, all 20 original public routes/metadata/bodies and screenshot hashes preserved. Homepage/topics/archives/Tools/TryHackMe/HackTheBox/404 remain present; future-type activity fixtures pass. Lockfile remains unchanged.

Browser suite intentionally excluded from deployment CI: no visual changes, no heavyweight runner setup. No new screen-reader/browser verification claimed. Existing known `h4cked` editorial warnings remain untouched.

GitHub-hosted validation: NOT RUN. Future hosted risks include remote Pages/default-branch/environment configuration, Actions policy, runner/prebuilt Ruby availability, third-party action/dependency availability and first hosted workflow parsing/execution. Local policy checks do not prove hosted success. Activation, validation-only preview, launch, smoke checks and source-revert rollback are documented in the runbook.

Proposed Phase 6: explicit user-reviewed commit/merge and Pages/environment activation, validate hosted CI/artifact, authorize launch, verify live routes/assets/accessibility, record deployment SHA and rollback baseline. No Phase 6 action performed.
