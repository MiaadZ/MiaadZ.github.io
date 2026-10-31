# Publication runbook

## Architecture and branch

Source → GitHub Actions → locked Ruby/Bundler/Jekyll with `_plugins/notebook.rb` → `_site` → Pages artifact → Pages deployment. Native Pages safe-mode Jekyll cannot run the required custom plugin. No output branch, generated HTML commits, PAT, custom secret, domain or CNAME is needed.

Publication branch: `main`, established from local `refs/remotes/origin/HEAD` (`origin/main`). Remote settings were not queried or changed. Confirm this remains the intended publication branch before launch. The redesign is currently on `mwga-redesign`; Phase 4 changes were already uncommitted when Phase 5 began. The user must review and commit the complete approved source before any later launch.

## Workflow behavior and security

`.github/workflows/pages.yml` builds PRs targeting `main`, pushes to `main`, and manual runs. PRs never deploy. Manual runs default to validation only; deployment requires the boolean `deploy` input and a run on `main`. Pushes to `main` publish after successful checks once Pages is manually activated. Therefore merging/pushing this workflow to `main` is a launch action, not a harmless preview.

Build permissions: `contents: read`, `pages: read` (Pages metadata lookup only). Deployment permissions: `contents: read`, `pages: write`, `id-token: write`. All other permissions default to none. Checkout disables persisted credentials. Full history is required for preservation comparisons against the immutable pre-migration commit. No `pull_request_target`, custom token or shell interpolation of event expressions is used. Event hashes used for whitespace comparisons are validated and passed as subprocess arguments.

`configure-pages` runs only for publication, with `enablement: false`; its pinned API source reads existing Pages configuration and cannot activate Pages through this path. PR and manual validation do not require Pages activation. No static-generator configuration rewrite is requested. Unexpected nonempty Pages base paths fail validation: this user-site publishes at `/`, retaining case-sensitive `/TryHackMe/*.html` routes. A future root custom domain remains possible after separately reviewing configuration.

Build jobs cancel superseded builds for the same PR/ref. Deployment has separate `pages` concurrency with `cancel-in-progress: false`, preserving a running deployment and replacing obsolete pending work. Concurrency is not a FIFO guarantee. The standard `github-pages` environment is used; recommend manually restricting deployment branches to `main`, optionally requiring a reviewer. No environment settings were changed here.

All action references are immutable commit SHAs resolved from their official repositories during Phase 5:

| Action | Reviewed version | Commit |
| --- | --- | --- |
| actions/checkout | v6 | d23441a48e516b6c34aea4fa41551a30e30af803 |
| actions/configure-pages | v5 | 983d7736d9b0ae728b81ab479565c72886d7745b |
| ruby/setup-ruby | v1 branch | de492cf36cbab201753d720ce4f4e336cd688c94 |
| actions/upload-pages-artifact | v4 | 7b1f4a764d45c48632c6b24a0339c27f5614fb0b |
| actions/deploy-pages | v4 | d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e |

Pins prevent moving tags from silently replacing workflow code. Review upstream changes before updating pins. `ruby/setup-ruby` is third-party executable build code: it downloads prebuilt Ruby and runs Bundler, so it remains a supply-chain trust boundary even when pinned. It reads `.ruby-version`, uses `BUNDLED WITH` from `Gemfile.lock`, and caches locked build gems in repository-local `vendor/bundle`. Existing lockfile checksums and frozen mode protect dependency resolution; no new gem dependency was introduced. Hosted runner images, action runtimes and upstream availability are still external dependencies.

Official references: [Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [Ruby setup pinned inputs](https://github.com/ruby/setup-ruby/blob/de492cf36cbab201753d720ce4f4e336cd688c94/action.yml), [Pages configuration API behavior](https://github.com/actions/configure-pages/blob/983d7736d9b0ae728b81ab479565c72886d7745b/src/api-client.js).

## Local and CI validation

Ruby `3.4.10`, Bundler `4.0.3`, Jekyll `4.4.1`; runner `ubuntu-24.04`. CI uses the committed root Gemfile/lock and Bundler caching. Local existing gems are under `docs/vendor/bundle`; no installation was needed in Phase 5.

```sh
export BUNDLE_FROZEN=true JEKYLL_ENV=production PAGES_BASE_PATH=''
# Existing local dependency location; CI setup-ruby uses vendor/bundle instead.
export BUNDLE_PATH="$PWD/docs/vendor/bundle"
python3 docs/verify-publication.py
bundle exec jekyll build --trace --destination _site --baseurl "$PAGES_BASE_PATH"
ruby -c _plugins/notebook.rb
python3 docs/verify-writeups.py _site
python3 docs/verify-phase4.py _site
git diff --check
git diff --exit-code -- Gemfile.lock
```

CI includes YAML/publication policy validation, meaningful commit-range whitespace checking, frozen production build, plugin syntax, all 20 baseline bodies/assets/metadata/URLs, generated links/anchors, archives/compatibility pages, homepage/topics and in-memory future collection checks. Existing Phase 2 wrapper delegates to the same preservation verifier and adds no coverage. The optional pre-migration rendered snapshot is not committed and is not a CI prerequisite.

Browser/CDP, native 400% zoom and screenshots remain local review checks (`docs/verify-browser.py`), excluded from Pages CI to avoid Chrome/system setup. Phase 5 changes no presentation. No new browser verification or screen-reader test is claimed. The YAML check uses existing Ruby/Psych plus Python standard library; it is a local policy/syntax check, not a substitute for GitHub's workflow parser and runner.

## Manual activation and launch — later, user-operated

1. Review/commit all approved source and check the intended branch. Validate the workflow in a PR to `main` or a manual validation-only run when available. Review the generated artifact before publication.
2. On GitHub: **Repository → Settings → Pages → Build and deployment → Source → GitHub Actions**. Do not enable a custom domain yet.
3. Review `github-pages` environment branch protections (`main` only; optional required reviewer) and repository Actions policy allowing the pinned official/Ruby actions. No custom secret is required.
4. After explicit launch approval, merge/push the approved change to `main`, or manually run on `main` with `deploy: true`. A publication run before activation fails its Pages metadata lookup intentionally.
5. Confirm build checks and artifact upload are green, then deployment is green with the expected commit SHA and environment URL. Open homepage, `/writeups/`, `/topics/`, topic routes, `/tryhackme/`, `/hackthebox/`, `/tools/`, `/404.html` and historical case-sensitive writeup URLs. Inspect CSS/images, keyboard/mobile behavior and browser network requests. Only then consider hosted migration validated.

**GitHub-hosted validation has not run in Phase 5.** No push, deployment, Pages setting change or credential access was performed.

## Rollback

Identify the last known-good commit from the successful `github-pages` deployment and Actions run, using read-only `git log` as needed. The user should revert the offending source commit(s) through a reviewed corrective commit on `main` (for example `git revert <bad-commit>`), retaining this workflow and locked build definition. The successful corrected branch build publishes a replacement artifact. Do not force-push history or edit generated `_site`; generated output is rebuilt from source. For a failure before successful deployment, the prior successful site remains the reference. Review changes before rerunning an older run because doing so can republish old source.

## Troubleshooting

- Missing Pages metadata/404: activate Actions as Pages source manually; do not add an administrative token or enablement workaround.
- Deploy denied/pending: check event, `main`, manual input, environment protection, Actions policy and default token permissions. PR runs deliberately cannot deploy.
- Ruby unavailable on runner: check pinned setup-ruby release/prebuilt Ruby support and runner architecture; retain the exact version until a reviewed toolchain update is approved.
- Frozen bundle/checksum/platform error: ensure Gemfile and lock match, lock supports Linux, correct Bundler is used and dependencies are accessible. Update the lock only through an approved local dependency review; never disable frozen mode as a CI workaround.
- Missing baseline Git object: preserve `fetch-depth: 0` and repository history.
- Route/content/topic failure: correct source metadata or implementation against the approved manifest; do not weaken preservation checks or rewrite technical bodies.
- Nonempty base path: confirm this is still the user-site repository. Project-site or domain changes require a separately reviewed route strategy.
- Artifact upload/deploy failure: inspect Pages size/file/link constraints and Actions logs; upload only `_site`, never the source/vendor tree.

The inherited `h4cked` relative `10.10.10.10` link and literal `put.png` code rendering remain separately reviewable editorial issues.
