# Coding Conventions

**Analysis Date:** 2026-03-14

## Naming Patterns

**Files:**
- `server.js` - Node server entry point (lowercase, descriptive)
- `index.html` - Frontend entry points (lowercase)
- `package.json` - NPM configuration (lowercase, hyphens for package name)
- CSS custom properties use `--kebab-case` (e.g., `--sidebar-w`, `--accent`, `--espresso`)

**Functions:**
- camelCase consistently used throughout: `getProgress()`, `saveProgress()`, `updateUI()`, `toggleComplete()`, `goTo()`, `handleHash()`, `initTerminal()`, `connectWS()`, `sendToTerminal()`, `copyCode()`
- Descriptive names that indicate purpose: `updateUI()` over `update()`, `toggleSidebar()` over `toggle()`
- Event handler functions typically start with action verb: `toggle*`, `handle*`, `update*`, `send*`, `copy*`

**Variables:**
- camelCase: `TOTAL` (constants in uppercase), `STORAGE_KEY`, `ws`, `term`, `fitAddon`, `termConnected`, `dragging`, `progress`, `ch`, `el`, `btn`
- Single-letter variables acceptable in loops and short callbacks: `e` for event, `ch` for chapter, `el` for element, `btn` for button
- Semantic naming: `termConnected` not `connected`, `fitAddon` not `addon`

**Types & Constants:**
- `TOTAL`, `STORAGE_KEY` - Constants declared at module scope in UPPERCASE
- Storage keys are semantic and specific: `'humanity-crash-course'`, `'humanity-crash-exercises'`

## Code Style

**Formatting:**
- No explicit formatter detected (no prettier/eslint config)
- Indentation: 2 spaces (observed in server.js and inline scripts)
- Line length: No strict limit observed; lines typically 80-120 characters
- Semicolons: Consistently used
- Trailing commas: Not used in objects/arrays

**Linting:**
- No ESLint or other linter configured
- Code pattern suggests manual code review conventions

**Quote Style:**
- Single quotes preferred in JavaScript: `'ws://localhost:8767'`, `'#ch'`
- Template literals used for dynamic content: `` `#ch${ch}` ``
- Double quotes used in HTML attributes

**Spacing:**
- Consistent spacing around operators: `completed / TOTAL * 100`
- Single space after control flow keywords: `if (x)`, `while (x)`
- Method chaining with direct dot notation: `document.getElementById().classList.toggle()`

## Import Organization

**Module Pattern:**
- CommonJS `require()` in Node files: `const { WebSocketServer } = require('ws');`
- Destructuring imports: `const { WebSocketServer } = require('ws');`
- Simple require statements at top of file: `const pty = require('node-pty');`, `const os = require('os');`

**Global Scope in Browser:**
- Vanilla JavaScript with no bundler
- Global `window` object extended with xterm library
- Direct access to DOM via `document` global
- LocalStorage and navigation APIs used directly

**No Path Aliases Detected**

## Error Handling

**Patterns Observed:**
- Try-catch with empty catch blocks for silent failure: `try { ... } catch { return {}; }`
- Selective catch blocks: `try { ws.send(...) } catch (e) { /* ws closed */ }`
- Inline inline checks before operations: `if (ws && ws.readyState === 1) ws.send(...)`
- Defensive programming with null coalescing and optional operations

**Error Strategy:**
- Silent failures acceptable for non-critical operations (WebSocket disconnects, JSON parse errors)
- Comments explain why failures are ignored: `catch (e) { /* ws closed */ }`
- No error logging framework; failures logged to console only when necessary

**Validation:**
- Input validation minimal; relies on try-catch
- Array/object existence checked before access: `if (msg.type === 'output')`
- State validation before operations: `if (ch >= 1 && ch <= TOTAL)`

## Logging

**Framework:** No logging library; `console.log()` used for server output

**Patterns:**
- Server startup logging with ANSI color codes: `console.log('\x1b[32m✓\x1b[0m Terminal server running on ws://localhost:${PORT}')`
- Event logging on connection/disconnection: `console.log('\x1b[32m✓\x1b[0m Browser connected')`
- Connection status indicated with colored symbols: `✓` (green), `○` (yellow)
- No client-side logging to console (clean user experience)

**When to Log:**
- Server lifecycle events (startup, connection, disconnection)
- No debug logging in production code
- User-facing actions (complete, navigate) tracked via localStorage instead

## Comments

**When to Comment:**
- Minimal commenting; code is self-documenting
- Comments used for non-obvious intent or workarounds: `/* ws closed */`, `/* ignore malformed */`
- Separator comments used for logical sections: `// ═══════════ SIDEBAR ═══════════`
- Comments on storage keys explaining purpose: `const STORAGE_KEY = 'humanity-crash-course';`

**No JSDoc/TSDoc**
- No function documentation strings
- No type annotations (vanilla JavaScript)

## Function Design

**Size:**
- Functions typically 10-30 lines
- Longer functions allowed for related operations: `initTerminal()` ~22 lines, `updateUI()` ~32 lines
- Single responsibility preferred: `getProgress()`, `saveProgress()` separate from UI updates

**Parameters:**
- Functions accept event objects: `function goTo(ch)`, `function sendToTerminal(text, btn, e)`
- Parameters typically 1-3 per function
- Event handlers receive event as last parameter: `copyCode(btn, e)`

**Return Values:**
- Most functions return void (side effects on DOM)
- Data functions return values: `getProgress()` returns object, `getExProgress()` returns object
- Try-catch blocks return default values on error: `return {}` or `return false`

## Module Design

**Exports:**
- Server exports via module.listener pattern (Node implicit globals)
- No explicit exports in HTML/JavaScript files
- Global function scope for browser interoperability

**Barrel Files:**
- Not applicable (no module system)
- HTML files act as entry points

## DOM Manipulation Patterns

**DOM Query Methods:**
- `document.getElementById()` for ID-based access
- `document.querySelectorAll()` for CSS selector queries
- `document.querySelector()` for single element selection

**Element Selection:**
- Semantic data attributes used: `data-ch` (chapter), `data-ex` (exercise)
- Class-based state management: `.active`, `.completed`, `.done`, `.open`
- Attribute selectors for data attributes: `.nav-item[data-ch="${ch}"]`

**Class Manipulation:**
- `.classList.toggle()` for boolean toggles
- `.classList.add()` and `.classList.remove()` for explicit control
- Chained operations common: `section.classList.add('active')` followed by `.remove('active')`

## WebSocket Communication

**Protocol:**
- JSON message format: `{ type: 'input|output|resize', data: ... }`
- Message types clearly named: `'input'`, `'output'`, `'resize'`
- Client initiates connection; server maintains listener

**Message Passing:**
- Validation on parse: `try { JSON.parse(msg) } catch`
- Type-based routing: `if (parsed.type === 'input') { ... }`

---

*Convention analysis: 2026-03-14*
