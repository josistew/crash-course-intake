# Codebase Structure

**Analysis Date:** 2026-03-14

## Directory Layout

```
crash-course-intake/
├── .git/                           # Git repository metadata
├── .github/
│   └── workflows/
│       └── pages.yml               # GitHub Actions: deploy to GitHub Pages
├── .gitignore                      # Git ignore rules
├── .planning/
│   └── codebase/                   # GSD codebase analysis documents
├── course/                         # Main interactive course (terminal-enabled)
│   ├── index.html                  # Course with embedded terminal (3606 lines)
│   ├── server.js                   # WebSocket + PTY backend
│   ├── package.json                # Dependencies: node-pty, ws
│   ├── package-lock.json           # Locked dependency versions
│   └── node_modules/               # Installed packages (not committed)
├── rez/                            # Rez variant crash course
│   ├── index.html                  # Rez's main course page
│   └── followup.html               # Rez follow-up/assignment content
├── JOSI-CRASH-COURSE.md            # Josi curriculum (text reference, ~500 lines)
├── REZ-CRASH-COURSE.md             # Rez curriculum (text reference, ~700 lines)
├── josi-motomedi.md                # Josi-specific project notes
├── rez-monday-gameplan.md          # Rez session agenda and takeaways
├── rez-motomedi.md                 # Rez business notes (Moto Medi + Tikka Shack)
├── index.html                      # Landing page (897 lines)
├── course.html                     # Course variant/bridge page (665 lines)
└── JOSI-CRASH-COURSE.md            # Full curriculum guide
```

## Directory Purposes

**`course/`:**
- Purpose: Self-contained Node.js terminal server + HTML5 course interface
- Contains: Backend server (JavaScript), frontend course SPA, manifest
- Key files: `server.js`, `index.html`, `package.json`
- Rationale: Isolated so `npm start` launches both frontend and backend in one step

**`rez/`:**
- Purpose: Alternative curriculum variant tailored to Rez (restaurant operator, non-technical)
- Contains: HTML course pages (no code editor)
- Key files: `index.html`, `followup.html`
- Rationale: Completely separate from main course; can be deployed independently

**`.github/workflows/`:**
- Purpose: CI/CD for GitHub Pages deployment
- Contains: GitHub Actions YAML configuration
- Key files: `pages.yml`
- Rationale: Auto-publishes on push to main branch

**`.planning/codebase/`:**
- Purpose: GSD (Get Stuff Done) codebase analysis documents
- Contains: ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md, TESTING.md, CONCERNS.md
- Key files: All .md files written by GSD mapper
- Rationale: Consumed by `/gsd:plan-phase` and `/gsd:execute-phase` orchestrators

## Key File Locations

**Entry Points:**

- `course/index.html`: Main crash course with terminal (3606 lines, includes inline CSS + JS)
- `index.html`: Landing page describing both courses (897 lines)
- `course/server.js`: Terminal server backend (50 lines, minimal)
- `rez/index.html`: Rez variant course

**Configuration:**

- `course/package.json`: Dependencies (node-pty, ws) and start script
- `course/package-lock.json`: Locked versions for reproducible installs
- `.github/workflows/pages.yml`: GitHub Pages deployment config

**Core Logic:**

**Frontend (Browser):**
- Navigation: `goTo(ch)` function dispatches chapter changes (lines ~3390–3410)
- Terminal UI: `initTerminal()` creates xterm.js instance (lines 3473–3494)
- WebSocket: `connectWS()` establishes connection, `sendToTerminal()` sends input (lines 3496–3535)
- Progress tracking: `completeExercise()` saves to localStorage (lines 3581–3589)
- Exercise UI: Toggle handlers for expandable exercise blocks (lines 3571–3579)

**Backend (Node.js):**
- Server bootstrap: WebSocket server on port 8767 (line 8 in `server.js`)
- PTY spawning: `pty.spawn(shell, ...)` creates terminal process (lines 17–23)
- I/O relay: `ptyProcess.onData()` → forward to client (lines 25–28)
- Input handling: Parse `type: 'input'` messages, write to PTY (lines 30–39)
- Cleanup: Close WebSocket on PTY exit, kill PTY on disconnect (lines 41–49)

**Styling:**

- All CSS embedded in `<style>` tags within HTML files
- Color system uses CSS variables: `--ink`, `--paper`, `--accent`, `--sage`, etc. (defined in `:root` blocks)
- Responsive layout: Flexbox for sidebar, terminal panel, main content (desktop-first, some mobile adjustments)

## Naming Conventions

**Files:**

- HTML: `index.html` for main pages (multiple variants in different dirs)
- Server: `server.js` (Node.js convention)
- Manifests: `package.json`, `package-lock.json`
- Config: `.github/workflows/*.yml` (GitHub Actions standard)
- Documentation: `UPPERCASE.md` for curriculum/notes, lowercase for project docs

**Directories:**

- Functional grouping: `course/` (main), `rez/` (variant), `.github/` (automation)
- Convention: lowercase with hyphens for multi-word names

**CSS Classes (in HTML):**

- BEM-like convention with hyphens: `.sidebar`, `.sidebar-nav`, `.nav-item`, `.chapter`, `.exercise`, `.code-block`
- State classes: `.active`, `.open`, `.done`, `.connected`, `.visible`
- Utility-style: `.primary`, `.sent`, `.copied`

**JavaScript Functions (in HTML):**

- camelCase: `goTo()`, `toggleSidebar()`, `initTerminal()`, `connectWS()`, `sendToTerminal()`, `completeExercise()`
- Boolean getters: `getExProgress()` returns state object
- UI updaters: `updateUI()`, `updateExUI()`, `updateTermStatus()`
- State togglers: `toggleExercise()`, `toggleExpected()`, `toggleComplete()`, `toggleTerminal()`

**Data:**

- LocalStorage key: `humanity-crash-exercises` (hyphenated brand name + entity)
- WebSocket message types: `"input"`, `"output"`, `"resize"` (lowercase, quoted strings)
- Chapter IDs: `ch1`, `ch2`, ... `ch9` (prefix + number, no padding)

## Where to Add New Code

**New Feature (e.g., add new chapter):**

1. Primary code: Add `<section class="chapter" id="ch10">...</section>` in `course/index.html` after line ~3400 (before closing body)
2. Tests: No formal test suite; validate by opening course in browser and testing navigation/terminal
3. Update constants: Change `const TOTAL = 9;` to `const TOTAL = 10;` (line ~3350)
4. Styling: Add CSS for `.chapter` variants in the `<style>` block (keep with existing chapter styles, ~400–800 line range)

**New Terminal-Enabled Variant:**

1. Copy `course/index.html` to new location (e.g., `advanced/index.html`)
2. Update `<title>`, logo, branding in `<head>` and sidebar
3. Modify chapter content/exercises as needed
4. Ensure `server.js` is still accessible at `ws://localhost:8767` (or update WebSocket URL)
5. Deploy: Point GitHub Pages to new HTML or use separate GitHub Pages repository

**New Non-Terminal Variant (like Rez):**

1. Create `/{variant}/index.html` (copy structure from `rez/index.html`)
2. Remove terminal-related HTML: delete `#terminalPanel`, `#xtermContainer`, `#terminalResize`, `#terminalOffline`
3. Remove terminal JavaScript: delete `initTerminal()`, `connectWS()`, `sendToTerminal()`, and WebSocket code (lines 3462–3535)
4. Keep navigation, chapters, exercises, styling
5. Remove "Send to Terminal" buttons; keep only "Copy" for code blocks

**New Utility Function:**

- Location: Add inside `<script>` block in `course/index.html` (around lines 3300–3600)
- Pattern: Use camelCase, prefix state with `let`, follow existing function style (no async/await observed)
- Example:
  ```javascript
  function myNewFunction(param) {
    // Do something
    return result;
  }
  ```

**Curriculum Content Update:**

1. For course text variants: Edit `JOSI-CRASH-COURSE.md` or `REZ-CRASH-COURSE.md`
2. For HTML course chapters: Edit section in `course/index.html` (search for chapter number)
3. For follow-up resources: Edit `rez/followup.html` or create new file in root

## Special Directories

**`node_modules/`:**
- Purpose: Installed npm dependencies
- Generated: Yes (via `npm install` from `package-lock.json`)
- Committed: No (listed in `.gitignore`)
- Size: ~650+ MB (node-pty includes native bindings)

**`.git/`:**
- Purpose: Git repository history and metadata
- Generated: Yes (via `git init`)
- Committed: N/A (git internals)

**`.github/`:**
- Purpose: Repository metadata and automation
- Generated: No (checked in)
- Committed: Yes

**`.planning/codebase/`:**
- Purpose: GSD documentation (ARCHITECTURE.md, STRUCTURE.md, etc.)
- Generated: Yes (by GSD mapper tools)
- Committed: Yes (checked in after generation)

## Build & Deployment

**Local Development:**

```bash
cd course
npm install                    # Install node-pty, ws
npm start                      # Starts server on ws://localhost:8767
# Then open http://localhost:PORT in browser
# (no local HTTP server included; rely on GitHub Pages or manual http.server)
```

**Production (GitHub Pages):**

- Triggered by: Push to `main` branch
- Workflow: `.github/workflows/pages.yml`
- Process: Uploads entire repo as static site to GitHub Pages
- Result: All HTML files accessible at `https://username.github.io/crash-course-intake/`
- Limitation: Terminal server (`server.js`) cannot run on GitHub Pages (no Node.js runtime); users must run locally or access separately

**Serving Landing Pages Locally:**

```bash
python3 -m http.server 8000        # Serve current directory
# Then open http://localhost:8000/index.html
```

---

*Structure analysis: 2026-03-14*
