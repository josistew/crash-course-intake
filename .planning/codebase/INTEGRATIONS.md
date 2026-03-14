# External Integrations

**Analysis Date:** 2026-03-14

## APIs & External Services

**Not detected** - No third-party API integrations are used in this codebase.

## Data Storage

**Databases:**
- Not used - Application is stateless

**File Storage:**
- Local filesystem only - Static HTML and course files served locally
- Course content stored in: `course/index.html`

**Caching:**
- Browser localStorage - Used for exercise progress tracking
  - Storage key: `'humanity-crash-exercises'`
  - Stores JSON stringified exercise completion state
  - No server-side caching

## Authentication & Identity

**Auth Provider:**
- None - Application requires no authentication
- No login, user identification, or session management
- All users access the same public course content

## Monitoring & Observability

**Error Tracking:**
- Not configured - No error reporting service

**Logs:**
- Console output only
  - Server logs: Terminal connection status via `console.log()` with colored output
  - Browser: No persistent logging

## CI/CD & Deployment

**Hosting:**
- Vercel deployment mentioned in course materials (`vercel --prod`)
- Currently serves static files locally via Node.js server

**CI Pipeline:**
- Not configured - No CI workflow present in `.github/`

## Environment Configuration

**Required env vars:**
- None - Application is zero-configuration
- Optional: `process.env.SHELL` - Shell preference (defaults to 'zsh' on Unix, 'powershell.exe' on Windows)

**Secrets location:**
- No secrets management required
- No `.env` files needed

## WebSocket Communication

**Incoming (Client → Server):**
- `ws://localhost:8767` - Terminal input channel
  - Payload type: `{ type: 'input', data: <string> }` - Terminal keystrokes/commands
  - Payload type: `{ type: 'resize', cols: <number>, rows: <number> }` - Terminal resize events

**Outgoing (Server → Client):**
- Terminal output channel
  - Payload type: `{ type: 'output', data: <string> }` - PTY process output

## Terminal Integration

**Shell Execution:**
- Spawns user's default shell via `node-pty`
- Inherits environment variables from parent Node process
- Supports terminal-specific env var: `TERM=xterm-256color`
- PTY dimensions: 80 columns × 24 rows (default), resizable

## Browser APIs

**Clipboard Access:**
- `navigator.clipboard.writeText()` - Copy button functionality for code snippets
- No clipboard reading

**Font Loading:**
- Google Fonts (https://fonts.googleapis.com)
- Fontshare API (https://api.fontshare.com)

---

*Integration audit: 2026-03-14*
