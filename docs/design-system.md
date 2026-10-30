# Design and presentation specification

Phase 1: specifications only; no CSS, markup or motion implementation.

## Identity
70–80% modern technical publication, 20–30% terminal accents. No fake terminal, Matrix rain, résumé, corporate SaaS hero or recruiting CTA.
Terminal cues belong in the hero prompt, metadata, code and small footer details, not navigation mechanics.

## Color tokens
Candidate tokens, subject to rendered contrast validation before approval:
- background #101216; surface #181c23; border #343d4b
- text #e8edf4; muted #a9b4c3
- primary/link #74b7ff; terminal #69d39c
- featured #e4c56d; warning/severity #ff8585
Use dark text on light accent fills, not white on green. Avoid tiny low-contrast metadata. Blue is primary; green is restrained; gold means featured, red means actual warning/severity, not generic difficulty fallback.
Text contrast: at least 4.5:1 normal, 3:1 large; meaningful UI boundaries/focus at least 3:1 against adjacent colors. Verify every state/pair, not just a palette.

## Type, measure and rhythm
System sans stack for prose; system monospace for code, paths and small labels; no external font requests.
Base 1rem minimum, article approximately 1.0625rem with line-height 1.7; permit browser zoom and user font settings. Main prose max-width 72ch. Wider shell up to 76rem; code/table blocks stay contained rather than widening the viewport.
Spacing scale .25, .5, .75, 1, 1.5, 2, 3, 4rem. Use normal document flow, not br tags for spacing.
One meaningful H1 per document. Predictable H2/H3 progression for new content. Existing heading text/IDs are protected; report old irregularities instead of rewriting them.

## Content surfaces
Links: visibly distinguishable, underline in prose, clear hover/focus and visited state; do not use color alone for state.
Code: local syntax styling from Jekyll/Rouge, monospace, horizontal scroll with visible affordance; preserve whitespace and exact content. No default copy-button JS.
Tables: readable header cells, row separation and a contained horizontal-scroll strategy; keyboard access must be tested. Do not automatically reinterpret arbitrary HTML/code as table headings.
Images/screenshots: intrinsic proportions, max-width:100%, height:auto, preserved original URLs and bytes. Keep readable access to original screenshots. Do not force shallow screenshot strips to an arbitrary height.
Cards/list entries: quiet separators or subtle surface, title and type/date first, optional factual summary. Avoid a dashboard of oversized decorative cards.
Tags/topics: wrapping text links; one normalized slug convention. Topics are knowledge navigation; tags are metadata.
Featured: gold border/icon plus explicit Featured text, never color alone.
Focus: visible :focus-visible outline with offset; do not remove browser outline without replacement. Hover and focus affordances should be equivalent; controls have accessible names.

## Responsive/accessibility behavior
Mobile-first, no minimum viewport assumption. Start one column; optional contents/sidebar only when enough space exists. Navigation wraps or uses native disclosure; never depends on JS to expose links.
At 320 CSS px and 400% zoom, no page-level horizontal scrolling; code/tables may scroll locally. Metadata wraps, flex children use min-width:0. Test long titles, empty summaries and wide terminal output.
Default shell includes skip link, lang=en, nav label, aria-current and one main landmark. Decorative icons/binary are aria-hidden; never hide the actual title with display:none.
No animation needed to understand content. Respect forced colors and preserve focus under reduced motion.

## Motion, later only
Actual brand text remains stable/readable. Brief CSS-only hover/focus glitch uses decorative duplicates, no flashing or layout movement.
Cursor may blink briefly on initial load then settle. No infinite animation.
Exact binary motif: 01010011 00110011 01011010 00110100 01010010
Use a static, faint hero/header fragment initially, never moving binary behind article text.
Transitions approximately 120–180ms for color/border; do not animate reading position.
prefers-reduced-motion disables glitch/cursor/keyframe motion and smooth scrolling. No third-party libraries, canvas rain or mandatory command UI.

## CSS organization
assets/css/main.scss imports, in order:
1. tokens: color, spacing, measure, type and motion custom properties.
2. base: reset, document defaults, links, headings, skip/focus behavior.
3. shell: header/nav/main/footer and responsive layout.
4. components: entries, badges, topic links, featured/empty states.
5. article: prose, code/highlighting, tables and images.

Keep component-specific media rules beside their rules; keep shared reduced-motion/forced-colors overrides in base. Do not create one partial per tiny component. No inline styles in new templates, no external CSS/CDNs and no CSS framework. Preserve raw inline HTML inside old bodies; treat any future cleanup as separate editorial work.
