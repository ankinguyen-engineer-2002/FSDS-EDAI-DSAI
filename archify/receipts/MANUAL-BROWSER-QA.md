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
