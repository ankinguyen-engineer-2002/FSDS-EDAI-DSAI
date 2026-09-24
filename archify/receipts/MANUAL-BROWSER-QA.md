# Manual browser QA — embedded Archify artifacts

Date: 2026-09-24
Runner: Playwright browser session against local static server.

## Automated Archify evidence

- 35/35 specs passed `validate --quality showcase` with `composition: pass`, 0 errors and 0 warnings.
- 35/35 artifacts passed `deliver --quality showcase` and have deterministic SHA-256 receipts in this directory.
- Packaged `visual-check` was attempted for every artifact, but the packaged Chrome DevTools process terminated with `SIGABRT` in this execution environment. Those JSON receipts are retained and are **not** claimed as passing browser evidence.

## Supplementary browser evidence

The delivered artifacts were then loaded through their exact committed HTML paths inside `fsds-learning-hub.html` using Playwright:

- all three Linux iframe paths were present;
- all three Python iframe paths were present;
- all three PostgreSQL iframe paths were present;
- F01/F02/F03 render 10/11/14 Archify labs respectively (35 total); all 35 lazy iframes were scrolled into view, reached `document.readyState = complete` and exposed an SVG document;
- lazy off-screen iframes loaded when each lab was scrolled into view;
- no browser console errors or warnings after removing unnecessary iframe sandbox flags;
- document/main overflow checked at 1440×900, 1024×768, 768×1024 and 390×844;
- note drawer, autosave, Escape close and per-topic note key were exercised, with the pre-test note restored afterward;
- window-based reading progress updated and persisted the per-topic scroll position;
- Python project/dependency section was found after render;
- light/dark, desktop rail collapse, mobile syllabus drawer/backdrop and mobile note drawer were exercised;
- final smoke test after the 35/35 migration and width expansion produced no page errors, console errors or console warnings.

- expanded desktop canvas measured 1552px with the 304px rail open and 1800px with the rail collapsed on a 1920px viewport;
- native lesson diagrams are no longer rendered in F01–F03.

## GitHub Pages production check

- Pages workflow run `35948532075` completed successfully on 2026-09-24.
- Production root returned HTTP 200.
- A delivered Archify artifact returned HTTP 200.
- Online Python lesson rendered 11 labs; the first iframe completed and exposed SVG with no horizontal overflow at 1440×900.

## Perceptual review

A visual inspection was performed on:

- desktop lesson opening;
- mobile Python lesson opening;
- desktop embedded Python runtime architecture (re-inspected after the final responsive edits).

Observed result: the Anthropic editorial shell and Archify field-note artifact are visually compatible. The embedded artifact reads as a visual lab inside the article rather than an unrelated application. No claim is made that this substitutes for user acceptance testing on every browser/OS.

## Canonical Linux/Tux mark check

After adding the digest-pinned mark captured from the official `kernel.org` site:

- five Linux artifacts were redelivered: command architecture, command execution, path/permission, synthesis and syscall boundary;
- each artifact reached `document.readyState = complete`, contained SVG, exposed exactly one `captured` brand node and one embedded `data:image` asset;
- all five reported zero page errors and zero horizontal overflow;
- the vendored audit copy `archify/brand-assets/linux-kernel-org.png` matches SHA-256 `9bfb70bf96004ac694b4ed902e634d029df9cc3b0ca50ce06d0608d29afa6d37`;
- the only console request observed during direct local opening was the static server's missing `/favicon.ico`; it is unrelated to the artifact and no runtime brand request was made.

## Beginner-first content and layout re-audit · 2026-09-24

After applying the four-part learning rule and rewriting the prose:

- 27 mechanism scenes across 19 chapters render from `content/lesson-mechanisms.json`;
- all three lessons render the required sequence: original pain → living metaphor → mechanism/stress test → one-line takeaway;
- each lesson renders 7 physical-to-technical metaphor mappings;
- F01/F02/F03 render 5/5/9 stress-test blocks and one golden takeaway each;
- the visible dictionary was deliberately pruned to 27/37/43 core term cards (107 total), backed by 182 practical examples;
- first chapter headings are plain-language questions and the first primer card is the physical metaphor, before the technical explanation;
- every Archify lab now has a visual-specific say-back line using that artifact's title and route.

Responsive matrix passed with zero horizontal overflow for F01, F02 and F03 at:

- 1920×1080;
- 1440×900;
- 1024×768;
- 768×1024;
- 390×844.

Canvas measurements:

- 1920 desktop with rail open: article width 1552px;
- 1440 desktop with rail open: article width 1084px;
- 1440 desktop with rail collapsed: article width 1388px;
- 390 mobile: article width 362px.

Archify runtime check:

- F01 10/10, F02 11/11 and F03 14/14 lazy iframes were scrolled into view;
- all 35 reached `document.readyState = complete` and exposed SVG;
- each iframe matched its viewport width with no internal horizontal overflow.

Interaction check:

- light/dark toggle changed the rendered theme without overflow;
- desktop rail collapse returned width to the article;
- note drawer opened, autosaved to the correct per-lesson localStorage key and closed with Escape;
- mobile syllabus opened with backdrop and closed with Escape;
- no JavaScript or browser console errors were present after the final reload.

Perceptual screenshots inspected locally:

- 1920px Linux opening: hero and pain card fill the row without the previous dead whitespace;
- loaded Database Archify lab: the artifact is readable directly in the article at full width;
- 390px Python opening: heading hierarchy, metadata and long Vietnamese title wrap without clipping.
