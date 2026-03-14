# Architecture

**Analysis Date:** 2026-03-14

## Pattern Overview

**Overall:** Monolithic educational platform with embedded interactive terminal and WebSocket-based client-server communication

**Key Characteristics:**
- Single-page application (SPA) with chapter-based navigation
- Real-time terminal emulation via WebSocket connection
- Decoupled frontend (HTML/CSS/JS) and backend (Node.js PTY server)
- Progressive enhancement: fallback to code copying when terminal unavailable
- Multi-audience curriculum (separate crash courses for Josi, Rez, course variants)

## Layers

**Frontend (Browser):**
- Purpose: Interactive course interface with embedded terminal, navigation, progress tracking, exercise completion
- Location: `course/index.html`, `index.html` (landing), `course.html`, `rez/index.html`, `rez/followup.html`
- Contains: HTML structure, CSS styling, vanilla JavaScript interactivity
- Depends on: xterm.js library (browser-side terminal emulation), WebSocket API
- Used by: End users (students/instructors) accessing crash course content

**Backend (Node.js Server):**
- Purpose: Spawn and manage pseudo-terminal (PTY) processes, relay I/O over WebSocket
- Location: `course/server.js`
- Contains: WebSocket server, PTY spawning logic, shell environment setup
- Depends on: `node-pty` (native terminal process), `ws` (WebSocket server)
- Used by: Frontend terminal to execute real shell commands

**Static Content:**
- Purpose: Marketing/informational landing pages and PDF-style crash course guides
- Location: Root-level markdown files (`JOSI-CRASH-COURSE.md`, `REZ-CRASH-COURSE.md`, `rez-monday-gameplan.md`, `rez-motomedi.md`)
- Contains: Instructional text, curriculum outline, success criteria
- Depends on: GitHub (rendering via .md files or HTML export)
- Used by: Attendees for reference and offline study

## Data Flow

**User Opens Course (Terminal Disabled):**

1. Browser loads `course/index.html` (3606 lines: HTML structure + CSS + inline JS)
2. JavaScript initializes xterm.js terminal emulator in container `#xtermContainer`
3. Browser attempts WebSocket connection to `ws://localhost:8767`
4. If successful: terminal becomes interactive → User types commands → Browser sends JSON `{"type": "input", "data": "..."}` over WS
5. Backend PTY receives command, executes in spawned shell, returns stdout/stderr
6. Backend sends JSON `{"type": "output", "data": "..."}` back over WS
7. xterm.js renders output in real-time

**User Opens Course (Terminal Unavailable):**

1. Connection attempt to `ws://localhost:8767` fails or times out after 3s retry loop
2. `updateTermStatus()` sets `termConnected = false`
3. Terminal UI shows offline message: `#terminalOffline` becomes visible
4. Code blocks show copy/send buttons: pressing copy uses `navigator.clipboard.writeText()` → user can paste into their own terminal

**Navigation & Progress:**

1. User clicks chapter nav or uses arrow keys (`ArrowRight`, `ArrowLeft`)
2. `goTo(chapter)` function: hides all `.chapter` elements, shows target chapter, updates sidebar active state, pushes to history
3. Progress tracked in `localStorage` under key `humanity-crash-exercises` as JSON object `{"1-1": true, "2-3": true, ...}`
4. Sidebar updates: `updateUI()` counts completed exercises, updates progress bar and counter

## Key Abstractions

**Terminal Emulation Client (`initTerminal()`):**
- Purpose: Initialize xterm.js terminal, connect WebSocket, handle I/O
- Examples: Lines 3473–3494 in `course/index.html`
- Pattern: Single global instance stored in `let term`, connected to `let ws`

**WebSocket Message Protocol:**
- Purpose: Bidirectional JSON messaging between browser and PTY server
- Examples: `{"type": "input", "data": "ls -la"}` (browser → server), `{"type": "output", "data": "..."}` (server → browser)
- Pattern: Type-based routing in both `server.js` (lines 30–39) and `course/index.html` (lines 3506–3508)

**Exercise Progress Persistence:**
- Purpose: Track user completion of hands-on exercises across browser sessions
- Examples: `completeExercise("4-1")` writes to `localStorage`, `getExProgress()` reads back
- Pattern: JSON serialization in localStorage; updates UI via `updateExUI()`

**Chapter Navigation State:**
- Purpose: Map between chapter IDs (ch1–ch9), displayed content, and URL hash
- Examples: `#ch4` in URL → `goTo(4)` → displays `#ch4` element
- Pattern: Hash-based routing with history API; `handleHash()` on page load and `popstate` events

## Entry Points

**Web Course (Terminal Server Required):**
- Location: `course/index.html`
- Triggers: User opens http://localhost:PORT (if serving locally) or GitHub Pages URL
- Responsibilities: Render multi-chapter curriculum, manage terminal connection, track exercise progress, provide navigation

**Terminal Server:**
- Location: `course/server.js`
- Triggers: `npm start` or `node server.js` in `course/` directory
- Responsibilities: Listen on `ws://localhost:8767`, spawn shell processes on connection, relay I/O bidirectionally, handle disconnection gracefully

**Landing Pages:**
- Location: `index.html`, `course.html`
- Triggers: User navigates to project root (GitHub Pages default)
- Responsibilities: Describe crash course, link to course variants, brand/positioning

**Curriculum Reference (Markdown):**
- Location: `JOSI-CRASH-COURSE.md`, `REZ-CRASH-COURSE.md`
- Triggers: User reads on GitHub or downloads for offline reference
- Responsibilities: Outline curriculum, prerequisites, learning objectives, success criteria

## Error Handling

**Strategy:** Graceful degradation with fallback modes; silent catches for non-critical failures

**Patterns:**

**Terminal Connection Loss:**
- `ws.onclose` → sets `termConnected = false` → shows offline UI → retries connection every 3 seconds
- User can still copy code blocks and paste into their own terminal (lines 3509–3513)

**Malformed WebSocket Messages:**
- Server: `try/catch` around `JSON.parse()` → silently ignores malformed input (lines 31–38 in `server.js`)
- Client: `try/catch` around `JSON.parse(e.data)` → silently ignores non-JSON (line 3507 in `course/index.html`)

**PTY Process Exit:**
- Server: `ptyProcess.onExit()` → closes WebSocket connection gracefully (lines 46–48 in `server.js`)
- Client: WebSocket close event handled, user sees offline message

**Missing Shell Command:**
- Delegated to PTY/shell: invalid command returns shell error message (e.g., "command not found")
- Error output rendered as normal terminal output

## Cross-Cutting Concerns

**Logging:**
- Server: Console logs connection/disconnection events with colored output (lines 10–12, 15, 42–43 in `server.js`)
- Client: No explicit logging; relies on browser DevTools

**Validation:**
- Exercise IDs: Checked against `TOTAL` constant (number of chapters) before navigation (lines 3428–3432)
- Chapter numbers: Must be integer between 1 and `TOTAL`
- WebSocket messages: Type field checked before routing (lines 33–37 in `server.js`, lines 3507 in `course/index.html`)

**Authentication:**
- None: Course runs in browser; no user accounts or login required
- Terminal access: Limited to localhost (not exposed over internet without additional server like Nginx)
- PTY environment: Runs as current user (not sandboxed)

**Security Considerations:**
- WebSocket runs on localhost only (line 6 in `server.js`: `ws://localhost:8767`)
- PTY spawned with user environment; no input sanitization (assumes trusted local user)
- No CSRF protection needed (no state-changing HTTP requests)
- Exercise progress stored in browser localStorage (unencrypted, client-editable)

---

*Architecture analysis: 2026-03-14*
