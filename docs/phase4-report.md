# Phase 4 — S3Z4R identity and curated notebook routes

## Outcome and boundaries
The final landing page, restrained CSS identity, six curated Topics, automatic mixed-content activity and conditional navigation are implemented.
All 20 technical writeup bodies remain byte-identical to the approved Phase 3 sources. Their only source-file change is reviewed topics metadata.
No Notes, Research or Projects were invented. No dependency, frontend JavaScript, third-party font/icon/animation package, analytics, tracker, comment system, résumé, employer/university biography or contact marketing was added.
No commit, push, merge, deployment, GitHub settings change, workflow or credential was created.

## Homepage structure and exact narrative
Order: hero/technical identity and narrative → three existing starred entries → Latest six published editorial entries → four selected topic routes → shared restrained TryHackMe footer link.
Identity: S3Z4R / Security Notebook.
Supporting statement: "Breaking, building and understanding systems."

Exact narrative:
> I started in software development, moved deeper into Linux and infrastructure, and eventually into security. This notebook is where I document the parts worth keeping: writeups, notes, research, experiments and tools.

Featured uses only existing starred metadata; no writeup was newly starred.
Latest combines published writeups, notes, research and projects, sorts date descending with title/URL tie-breaks, then applies its six-entry limit. Topics and ordinary pages are excluded.
Only writeups currently populate it. In-memory tests prove all four labels and future content types work without creating example source/output pages.

## Curated topics and evidence
Topics are explicit editorial relationships, not aliases for every tool tag.

| Topic | Current related writeups | Evidence/rationale |
|---|---:|---|
| Web Security | 9 | RootMe upload handling; Overpass session cookie behavior; Fuel CMS, elFinder and Bricks Builder exploitation; IIS/share misconfiguration; the Advent event's race-condition summary. |
| Linux Privilege Escalation | 9 | RootMe SUID; Wonderland imports/PATH/capabilities; Overpass/Skynet scheduled jobs; sudo-enabled tools and backup scripts in other linked labs. |
| Credential Attacks | 12 | Basic Pentesting SSH/key recovery; Tomghost PGP artifacts; FTP, web and SSH password testing; credentials recovered from shares/captures. |
| Enumeration | 8 | Basic Pentesting shares; Relevant full-port and SMB/IIS discovery; WordPress inspection and web-path discovery in the linked walkthroughs. |
| Network Forensics | 2 | h4cked reconstructs FTP activity in Wireshark; Startup examines suspicious.pcapng for an earlier session. |
| Reverse Engineering | 2 | Compiled and Wonderland contain debugger-guided inspection of binaries and execution/control-flow behavior. |

docs/topic-evidence.json records every membership, a specific existing section anchor and a factual rationale. All cited anchors were checked.
Each _topics page has a concise factual description, suggested starting links and automatically related published content grouped by type. Empty groups are omitted.
The homepage selects Linux Privilege Escalation, Network Forensics, Reverse Engineering and Web Security through the topics' featured flags. All six are in /topics/.
Each original writeup has at least one reviewed route; 42 relationships connect the 20 writeups to these six areas.
No summary, technique/tool list, updated date or factual article metadata was invented. Original tags remain unchanged. /tools/ remains the compatible legacy tag index, with its route toward Topics.

## Navigation and authoring
Decision B: primary navigation always exposes Writeups and Topics. Notes, Research and Projects are omitted while empty and appear automatically when published content exists.
Their direct archive URLs remain available with intentional minimal empty states.
The site identity links naturally home. Active page/section state uses aria-current.

The existing platform-neutral writeup template remains unchanged. A future author can create _writeups/thm-example.md, fill factual normalized front matter, write Markdown and build. Homepage, Latest, writeup/platform archives and tag indexes update automatically.
Reviewed topic slugs in front matter automatically connect content to topic routes and update their counts. Topic curation remains editorial: when reclassifying protected originals, maintain the documented review record. A genuinely new topic requires a real topic page and review. There is no manual list of articles in homepage/archive/platform templates.

The plugin now validates collection/type agreement and topic references, exports published topic routes/counts, and omits unpublished/future or status:draft entries from activity. No new runtime dependency is involved.

## Identity and finite motion
- Exact binary motif: 01010011 00110011 01011010 00110100 01010010.
- Binary is static, faint, responsive and aria-hidden; it appears only in the homepage hero.
- Brand glitch: one 180 ms blue clipped-copy pass on hover or keyboard focus. Movement is limited to 1 px; the real text remains at opacity 1 with no transform.
- Decorative copies are aria-hidden. The header identity supports keyboard focus naturally as a home link; the hero responds to interaction without turning into a terminal UI.
- Cursor: three 900 ms cycles after load, then static; no infinite animation.
- Reduced motion hides the glitch copy and disables animation, leaving a static cursor.
- Article prose has no binary or glitch background. The long-form width, code/table wrappers and screenshot source files remain intact.

CSS also maps the existing literal green paragraph cue in Compiled to the readable terminal-green token. Its source HTML and text are unchanged; computed contrast is 10.18:1. This is a narrow presentation compatibility rule rather than a prose edit.

## Build, preservation and verification
Jekyll 4.4.1 builds with the existing frozen lockfile and Ruby 3.4.10. No packages were installed or upgraded.
The original manifests and historical Phase 2/3 evidence remain unchanged.
The existing verification suite passes, including all 20 legacy routes, canonical paths, source links, metadata, original body/asset hashes and heading anchors.
Rendered code/output blocks and runtime asset references match the pre-Phase-4 build.
A direct Git comparison also proves each original source differs from Phase 3 only by its one topics metadata line; the approved authoring template and dependency files are unchanged.
The final build produces 36 HTML pages and no build warnings.

Commands:
```sh
BUNDLE_FROZEN=true BUNDLE_PATH="$PWD/docs/vendor/bundle" bundle exec jekyll build --trace
python3 docs/verify-writeups.py _site .jekyll-cache/phase4-baseline
python3 docs/verify-phase2.py _site
python3 docs/verify-phase4.py _site
python3 docs/verify-browser.py http://127.0.0.1:8844 http://127.0.0.1:9444
git diff --check
```

Browser verification:
- 80 views at 1440, 390 and 320 CSS px cover every writeup at narrow width and representative long-code/output, table, screenshot, Linux/Windows and raw-HTML content; home, navigation, featured/latest, all topic routes, archives and 404 are covered.
- Six additional native 400% Chrome page-zoom checks cover home, Topics index, a topic route, writeups, h4cked and 404.
- Native zoom is independently confirmed: 1280 px unzoomed layout → 320 CSS px, DPR 4, reflow ratio 4.0, visualViewport scale 1. This is browser page zoom, not CSS zoom/pinch/viewport-only emulation.
- No page-level horizontal overflow. Images load; code/table regions remain focusable and horizontally scrollable.
- Skip navigation, visible keyboard focus, native contents disclosure and ArrowRight code scrolling pass.
- The real identity text stays static; glitch/cursor animations settle; reduced motion disables them.
- Browser accessibility-tree inspection marks the decorative glitch/binary/cursor nodes ignored. Screen-reader software was not used; no screen-reader verification is claimed.
- Shared meaningful text/accent tokens exceed 4.5:1 on both dark surfaces; borders/focus exceed 3:1. The inherited green paragraph is now 10.18:1 at desktop/mobile widths.
- Desktop/mobile screenshots were visually reviewed. Other browser engines and manual screen-reader review remain later checks.

docs/phase4-verification.json preserves numeric browser/motion/zoom evidence, hashes, membership checks and runtime measurements.
Ignored preview artifacts are under .jekyll-cache/phase4/ and .jekyll-cache/phase4-baseline/; website output is _site/. None is published.

## Performance and runtime
Final generated CSS: 9332 bytes; gzip 2783 bytes.
Homepage HTML: 8034 bytes; gzip 1935 bytes.
Frontend JavaScript: 0 bytes. Homepage images: 0. No external runtime assets, CDNs or font requests are required.
The existing unused profile image remains a preserved source asset but is not referenced or loaded by the homepage.
Shared includes render short lists, not duplicated article bodies. Motion is interaction-triggered or finite at startup; it does not perform continuous background work.

## Hosting/build recommendation — analysis only
Recommendation: use GitHub Actions to build this existing Jekyll site with the root Ruby/Gemfile/lockfile and publish only the verified _site artifact in a later explicitly authorized phase.

Native GitHub Pages Jekyll enforces safe mode and cannot run unsupported plugins. This notebook uses a repository plugin, so forcing native compatibility would require replacing useful behavior. [GitHub Pages/Jekyll documentation](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll#plugins)

Assessment for this repository:

| Consideration | Native Pages Jekyll | Custom Actions build |
|---|---|---|
| Plugin support | Current notebook helpers cannot run as-is | Normal bundle exec Jekyll can retain them |
| Reproducibility/dependencies | Managed Pages build constraints | Existing pinned Ruby and frozen root lockfile |
| Maintainability | A separate Liquid/validation port to maintain | Same implementation and checks as local development |
| Security | Restricted managed build surface | Build executes reviewed repository code; permissions need explicit separation |
| Complexity | Simple hosting setup, substantial compatibility work here | A small explicit workflow to review; no presentation rewrite |

GitHub documents custom build/artifact workflows for Pages. Use a normal root-bundle build rather than assuming a managed Pages builder reproduces this project's plugins and versions. [Custom workflows documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

For a later workflow: keep the build read-only with no deployment secrets, separate any authorized deployment job, use narrowly scoped permissions and reviewed immutable action references or supported workflow dependency lockfiles, and avoid privileged execution of untrusted changes. [GitHub Actions secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use)
The preservation verifier needs the original Git objects identified by legacy-manifest.yml; a future checkout must retain/fetch that baseline history.
Upload only verified generated output, never the repository, docs, installed gems or editor artifacts.
Actual repository hosting settings were not queried or changed. No workflow draft, credentials, external service configuration or deployment was created.

## Known issues left unchanged
1. h4cked's relative 10.10.10.10 link remains.
2. h4cked's put.png reference still renders literally inside code. Eight images render; all nine screenshot files and reference paths are intact.
Both are separately reviewable editorial fixes and were not silently corrected.
Historical multiword raw tag fragments remain a compatibility review item; all currently emitted normalized anchors resolve.
Some narrow screenshots need zoom/full-resolution viewing; asset bytes were not modified.
Manual screen-reader and additional-browser review remain outstanding.

## Complete project file accounting
Created:
- _topics/credential-attacks.md
- _topics/enumeration.md
- _topics/linux-privilege-escalation.md
- _topics/network-forensics.md
- _topics/reverse-engineering.md
- _topics/web-security.md
- docs/phase4-report.md
- docs/phase4-verification.json
- docs/topic-evidence.json
- docs/verify-phase4.py

Modified:
- README.md
- _data/navigation.yml
- _includes/content-list.html
- _includes/header.html
- _layouts/archive.html
- _layouts/article.html
- _layouts/home.html
- _layouts/topic.html
- _plugins/notebook.rb
- _sass/_article.scss
- _sass/_components.scss
- _sass/_shell.scss
- _writeups/thm-advent-of-cyber-2025.md
- _writeups/thm-agent-sudo.md
- _writeups/thm-basic-pentesting.md
- _writeups/thm-brooklyn-nine-nine.md
- _writeups/thm-brute-it.md
- _writeups/thm-compiled.md
- _writeups/thm-cyborg.md
- _writeups/thm-h4cked.md
- _writeups/thm-ignite.md
- _writeups/thm-lazy-admin.md
- _writeups/thm-lookup.md
- _writeups/thm-mr-robot-ctf.md
- _writeups/thm-overpass.md
- _writeups/thm-relevant.md
- _writeups/thm-root-me.md
- _writeups/thm-skynet.md
- _writeups/thm-startup.md
- _writeups/thm-tomghost.md
- _writeups/thm-tryhack3m-bricks-heist.md
- _writeups/thm-wonderland.md
- docs/verify-browser.py
- docs/verify-writeups.py
- docs/writeup-workflow.md
- index.md
- topics.md

The 20 _writeups changes are topics metadata only. No technical body, command, output, flag, credential, date, attack chain, finding, remediation or screenshot changed.
Moved: none. Deleted: no project source files. Only temporary bytecode generated by a test compilation check was cleaned up.
No deployment/workflow/GitHub configuration files were created or changed.

## Proposed Phase 5 scope — not started
Review the homepage narrative and initial topic classifications locally.
Authorize any targeted h4cked editorial corrections separately, recording deliberate preservation exceptions without replacing the immutable baseline.
Complete manual screen-reader and secondary-browser review.
If explicitly authorized, prepare/review the custom Actions build and publication configuration. Deployment remains a separate approval/action.
No Phase 5 work has begun.
