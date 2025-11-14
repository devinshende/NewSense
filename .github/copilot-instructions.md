<!-- .github/copilot-instructions.md - tailored guidance for AI coding agents -->

# Agent Instructions for NLPDumbathon-2025

Purpose: quick, actionable guidance so an AI coding agent can be productive immediately in this repo.

- Repository type: static frontend demo (pure HTML + inline JS). No build tools, no package.json.
- Primary files to inspect: `index.html`, `canvas.html`, `README.md`, `attentionisallyouneed.txt`.

Key Architecture & Data Flow
- The app is a two-page static site: `index.html` (input form) -> `canvas.html` (animated display).
- Data is passed from input page to canvas via `localStorage.animationText` (see `index.html` startAnimation()).
- `canvas.html` reads `localStorage.getItem('animationText')` and transforms it with `contentTransforms` before rendering.
- Animation layer: the visual characters are DOM elements inside `#character-layer` and movement + effects are driven by GSAP (CDN import).

Critical Patterns & Where To Make Changes (concrete examples)
- Add new transformation mode: edit the `contentTransforms` object in `canvas.html` and add a matching `<option>` in the `#style-mode` `<select>`.
  - Example: in `canvas.html` search for `const contentTransforms` and add a new key/function.
- Change how text is split/displayed: update `splitParagraphs()` / `ParseInput()` in `canvas.html`.
- Tweak character movement or collision: modify `animateCharacter()` and `checkCollisions()` in `canvas.html`. Character size is controlled by CSS (`.character` width/height) and JS `charSize` variable — keep them in sync.
- Where file upload appears: `index.html` contains a file input (`#file_upload`) that is currently NOT processed — do not assume it alters flow unless you implement parsing and set `localStorage.animationText` or call the same submit flow.

External Dependencies & Runtime
- Tailwind CSS and GSAP are loaded from CDNs in the HTML files. There is no bundler; work is done directly in the browser.
- To run and debug locally, serve the directory with a static server (recommended):
  - `python3 -m http.server 8000` (run from project root) and open `http://localhost:8000/index.html`.
  - Note: accessing files with `file://` can cause inconsistent behavior for `localStorage` and module imports — use a local server.

Debugging Tips
- Inspect `localStorage.animationText` in the browser console to verify input text payload.
- Use browser DevTools to set breakpoints in inline scripts (open `canvas.html` -> Sources -> select the file).
- Grep for `contentTransforms`, `ParseInput`, `checkCollisions`, and `animateCharacter` to find the main logic quickly.

Project Conventions & Expectations
- Keep changes minimal and self-contained: this repository is designed as a small demo. Avoid adding heavy toolchains unless requested.
- Preserve inline scripts and CDN imports unless converting to a module/bundler is explicitly requested.
- Use clear, minimal diffs: prefer editing the existing HTML/JS rather than adding new build steps.

When making PRs
- Describe runtime verification steps in the PR body (how to run local server and reproduce the animation).
- If adding modes or animation behavior, include a short note with test input text and expected visible changes.

Searchable anchors (use these to locate behavior quickly)
- `index.html` — `startAnimation()` (entry point for input page)
- `canvas.html` — `localStorage.getItem('animationText')`, `contentTransforms`, `ParseInput`, `splitParagraphs`, `animateCharacter`, `checkCollisions`

Limitations (discoverable from code)
- No tests or automated checks present.
- No backend; all logic runs in-browser.
- File upload exists but is not wired to processing flow.

If you need to extend the project
- Ask before adding build tooling. Suggested minimal path: move inline scripts to a single `main.js`, keep CDN for libraries, and add a lightweight `package.json` only if necessary.

Questions for the maintainer (put these as PR comments if unclear)
- Do you want the file upload (`#file_upload`) to populate `animationText` automatically?
- Should the project be converted to a small node/static site with bundling, or remain CDN+static HTML?

---
Keep edits focused and testable by running a local static server and verifying `index.html` -> `canvas.html` flow.
