## Permission model

Codex may perform normal local development work inside this repository without stopping for confirmation.

### Allowed local actions

Codex may:

- read any file inside this repository
- create and modify project files required by an approved task
- move or rename project files according to an approved migration plan
- create Jekyll layouts, includes, Sass/CSS, configuration and documentation
- run local inspection commands
- run Ruby/Jekyll/Bundler commands required to build or validate the site
- run local tests, linters and validation commands
- run `git status`, `git diff`, `git diff --check`, `git log` and other read-only Git commands
- generate temporary build artifacts
- remove temporary build artifacts that it created
- update front matter mechanically where explicitly covered by an approved migration plan

### Approved dependency behavior

Codex may install build-only project dependencies declared in repository-controlled Gemfiles when required for an already approved implementation phase.

Dependency installation must:

- use Bundler
- remain local to the project where possible
- use `vendor/bundle` or another repository-local dependency path
- install only dependencies already declared in an approved Gemfile
- never use `sudo`
- never use system package managers
- never run arbitrary remote installation scripts
- never introduce a new dependency without explaining and obtaining approval first

Examples of allowed commands include:

`BUNDLE_PATH=vendor/bundle bundle install`

and commands using an approved alternate Gemfile.

### Actions still requiring explicit approval

Never perform these without explicit user approval:

- `git commit`
- `git push`
- `git merge`
- `git rebase`
- branch creation or deletion
- tag creation or deletion
- deployment
- GitHub repository configuration changes
- DNS changes
- Cloudflare changes
- changing remote repositories
- modifying Git configuration
- accessing or modifying credentials
- accessing secrets
- installing system packages
- using `sudo`
- modifying files outside this repository
- introducing a new runtime or build dependency
- destructive bulk deletion
- publishing content externally

## Network access

Network access should be minimal.

Allowed when necessary for an approved task:

- downloading dependencies declared in an approved project dependency file
- retrieving documentation required to resolve a concrete implementation issue

Do not:

- upload repository content
- transmit credentials
- call unrelated external services
- deploy
- publish
- interact with production infrastructure

## Existing content protection

Do not rewrite technical writeup prose unless explicitly requested.

Do not alter factual content including:

- commands
- command flags
- screenshots
- findings
- CTF credentials
- flags
- dates
- attack chains
- remediation conclusions

Mechanical migrations explicitly approved by the user are allowed, including:

- front-matter field normalization
- permalink addition
- `page.machine_url` to `page.source_url`
- source-file relocation
- formatting required by the new layout system

These changes must preserve technical meaning.

## Git policy

Codex may inspect Git freely using read-only commands.

Codex must not commit or publish changes.

At the completion of each implementation phase, report:

- files created
- files modified
- files moved
- files deleted
- build/test results
- unresolved issues

The user reviews and performs commits manually.

## Verification

Before declaring an implementation phase complete:

- run the Jekyll build when dependencies are available
- run `git diff --check`
- validate relevant internal links and routes
- verify image references
- verify unchanged writeup sources and assets against Git unless content edits were requested
- report warnings and errors
