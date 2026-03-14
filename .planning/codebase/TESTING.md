# Testing Patterns

**Analysis Date:** 2026-03-14

## Test Framework

**Runner:**
- Not detected - no test framework configured

**Assertion Library:**
- Not detected

**Run Commands:**
```bash
# No test command defined in package.json
# Only command available: npm start
```

## Test File Organization

**Current State:**
- No test files present in codebase
- No test directory (`tests/`, `__tests__/`, `test/`)
- No test configuration files (`jest.config.js`, `vitest.config.js`, `mocha.opts`, etc.)

**Location:**
- Not applicable - testing not implemented

**Naming:**
- No test files found
- No `.test.js` or `.spec.js` files in project root or subdirectories

**Structure:**
- Not applicable

## What Gets Tested

**Currently Tested:**
- Manual testing only via interactive UI
- Progress persistence tested through localStorage (manual)
- Terminal connection tested through WebSocket (manual)
- Code execution tested via browser console

**How It's Tested:**
- Interactive HTML UI allows manual verification of:
  - Chapter navigation (arrow keys, click)
  - Progress saving/loading (completion button)
  - Terminal connection status
  - Exercise tracking
  - Sidebar toggle and responsive behavior

## Testing Gaps

**Critical Untested Areas:**

**Server Logic (`/Users/josi/crash-course-intake/course/server.js`):**
- WebSocket connection handling
- PTY process spawning and lifecycle
- Process resize events
- Data serialization (JSON encode/decode)
- Process kill on client disconnect
- Error recovery and reconnection timing

**Client Logic (`/Users/josi/crash-course-intake/course/index.html` - JavaScript section):**
- `getProgress()` - localStorage parsing and error handling
- `saveProgress()` - localStorage write operations
- `updateUI()` - DOM element updates and state reflection
- `toggleComplete()` - completion state toggle logic
- `goTo()` - chapter navigation and history management
- `initTerminal()` - xterm initialization and configuration
- `connectWS()` - WebSocket connection, retry logic (3-second backoff)
- `sendToTerminal()` - message serialization and send confirmation
- `copyCode()` - clipboard write and UI feedback
- Keyboard navigation (arrow keys for chapter switching)
- Terminal resize handle drag behavior
- Exercise completion tracking

**No Test Coverage:**
- Progress persistence across sessions
- WebSocket message ordering and delivery
- Terminal output buffering
- Mobile responsive behavior
- Accessibility features
- Performance under load

## Testing Recommendations

**Priority 1 - Core Features:**
1. **LocalStorage Persistence**
   - Test `getProgress()` with valid/invalid JSON
   - Test `saveProgress()` writes correct format
   - Test round-trip: save → load → verify

2. **WebSocket Communication**
   - Mock WebSocket in browser tests
   - Test message serialization format
   - Test retry logic (connection drops after 3 seconds)
   - Test reconnection behavior

3. **PTY Process Management (server)**
   - Test process spawn with correct shell
   - Test data event forwarding
   - Test kill on client disconnect
   - Test resize commands

**Priority 2 - UI State:**
1. **Navigation Logic**
   - Test `goTo()` updates active chapter
   - Test hash-based navigation
   - Test arrow key navigation (left/right)
   - Test boundary conditions (first/last chapter)

2. **Progress UI Updates**
   - Test `updateUI()` reflects saved progress
   - Test completion button state toggle
   - Test progress bar calculation (completed / TOTAL)

**Priority 3 - Edge Cases:**
1. **Error Recovery**
   - WebSocket reconnection after timeout
   - Malformed JSON message handling
   - localStorage quota exceeded
   - PTY process unexpected exit

## Implementation Path

**Recommended Stack:**
- Runner: Vitest (fast, modern, good TypeScript support)
- Browser testing: Vitest + @vitest/browser (for DOM interaction)
- Server testing: Vitest with mock WebSocket/PTY
- Mock libraries: Node built-in mocks or Sinon.js

**Test File Structure:**
```
course/
├── server.js
├── server.test.js          # WebSocket/PTY tests
└── index.html
└── index.test.js           # DOM/progress/navigation tests
```

**Example Test Pattern - Progress Persistence:**
```javascript
// Would test:
describe('Progress Management', () => {
  it('saves and retrieves progress from localStorage', () => {
    const progress = { '1': true, '2': false };
    saveProgress(progress);
    const loaded = getProgress();
    expect(loaded).toEqual(progress);
  });

  it('returns empty object on localStorage error', () => {
    // Mock localStorage.getItem to throw
    const result = getProgress();
    expect(result).toEqual({});
  });
});
```

**Example Test Pattern - WebSocket:**
```javascript
// Would test:
describe('Terminal Connection', () => {
  it('connects to WebSocket and sends resize on open', () => {
    // Mock WebSocket
    // Trigger connectWS()
    // Verify ws.send called with resize message
    // Verify fitAddon.fit() called
  });

  it('reconnects after 3 seconds on disconnect', async () => {
    // Mock WebSocket.onclose
    // Wait 3 seconds
    // Verify connectWS() called again
  });
});
```

## Current Testing Approach

**Manual Verification Steps:**
1. Open `/Users/josi/crash-course-intake/course/index.html` in browser
2. Click "Mark Complete" on chapter
3. Reload page - chapter should still show "Completed"
4. Press arrow keys to navigate chapters
5. Click terminal toggle - should attempt to connect to `ws://localhost:8767`
6. Run `npm start` in `/Users/josi/crash-course-intake/course/` in separate terminal
7. Terminal should display in browser
8. Type commands in terminal and verify they execute
9. Close terminal or disconnect server - should show "Terminal offline" message
10. Restart server - should reconnect automatically within 3 seconds

**Known Limitations:**
- Time-consuming and error-prone
- Cannot verify internal state
- Difficult to test edge cases (network failures, race conditions)
- No regression testing on code changes
- Mobile/responsive testing requires manual device testing

---

*Testing analysis: 2026-03-14*
