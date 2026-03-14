# Technology Stack

**Analysis Date:** 2026-03-14

## Languages

**Primary:**
- JavaScript - Used for server and client code

**Secondary:**
- HTML - Course interface and content structure

## Runtime

**Environment:**
- Node.js v24.2.0 (development)

**Package Manager:**
- npm v11.3.0
- Lockfile: `package-lock.json` present in `/Users/josi/crash-course-intake/course/`

## Frameworks

**Core:**
- WebSocket Server (ws) v8.18.0 - Real-time terminal communication between browser and server
- xterm.js v5.5.0 - Browser terminal emulator UI
- xterm.js addon-fit v0.10.0 - Terminal resize and fit functionality

**Build/Dev:**
- Node.js native modules - No build system present

## Key Dependencies

**Critical:**
- `ws` v8.18.0 - WebSocket server library for real-time bidirectional communication
  - Peer dependencies: `bufferutil`, `utf-8-validate` (optional)
- `node-pty` v1.0.0 - Pseudo-terminal spawning for shell integration
  - Depends on: `node-addon-api` v7.1.0 for native module support

**Infrastructure:**
- `node-addon-api` v7.1.1 - N-API bindings for native module compilation

## Configuration

**Environment:**
- Shell configuration via `process.env.SHELL` (defaults to 'zsh' on Unix, 'powershell.exe' on Windows)
- Terminal settings hardcoded: xterm-256color mode, 80x24 default size
- Working directory: User's home directory (`os.homedir()`)

**Build:**
- No build configuration files present
- Single npm script: `npm start` → runs `node server.js`

## Platform Requirements

**Development:**
- Node.js v24.2.0 or compatible
- npm v11.3.0 or higher
- Platform support: Windows (powershell), macOS/Linux (zsh or $SHELL)
- Requires compile-time support for node-pty (uses native modules)

**Production:**
- WebSocket port 8767 must be accessible
- Static HTML file serving (course/index.html)
- No database or external service dependencies

## Fonts & UI Libraries

**CDN Resources:**
- Google Fonts API - Fraunces, Outfit, JetBrains Mono typefaces
- Fontshare API - Cabinet Grotesk font
- JSDelivr CDN - xterm.js library and stylesheets

---

*Stack analysis: 2026-03-14*
