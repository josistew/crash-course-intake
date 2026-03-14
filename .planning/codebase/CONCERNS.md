# Codebase Concerns

**Analysis Date:** 2026-03-14

## Security & Access Control

**No Authentication on WebSocket Server:**
- Issue: `ws://localhost:${PORT}` WebSocket server has no authentication or access control
- Files: `course/server.js` (lines 8, 14)
- Risk: Any client that can connect to the machine can spawn arbitrary shell commands via PTY access
- Current mitigation: Only binds to localhost, but no token-based auth or session management
- Recommendations: Implement WebSocket authentication token, session timeout, and connection rate limiting

**Arbitrary Shell Command Execution:**
- Issue: The PTY process spawns a shell with full user permissions and executes any input from WebSocket clients
- Files: `course/server.js` (lines 17-23, 33-34)
- Risk: No input sanitization or command filtering allows clients to execute any shell commands, view sensitive files, or modify the system
- Current mitigation: None
- Recommendations: Implement command allowlisting, input validation, or run PTY in a sandbox/container with restricted permissions

## Error Handling & Observability

**Silent Error Suppression:**
- Issue: All error handlers use inline comments to silently swallow exceptions: `catch (e) { /* ... */ }`
- Files: `course/server.js` (lines 27, 38, 47)
- Impact: Makes debugging difficult; unknown failures go unlogged; connection/data loss goes undetected
- Fix approach: Replace silent catches with proper logging. Log error type, message, and context. Example: `catch (e) { console.error('PTY write failed:', e.message); }`

**No Error Logging for Connection Failures:**
- Issue: WebSocket connection errors and PTY spawn failures have no logging
- Files: `course/server.js` (entire file)
- Risk: Server state problems (out of memory, file descriptor limits) go unnoticed until clients connect and fail
- Priority: Medium
- Recommendation: Add try-catch around PTY spawn with error logging. Add `wss.on('error')` handler.

**No Process Health Monitoring:**
- Issue: Server has no heartbeat, uptime tracking, or crash recovery mechanism
- Files: `course/server.js`
- Risk: Server could crash silently; no automatic restart; no alerting mechanism
- Improvement path: Add process monitoring via Node supervisor or systemd. Add periodic health checks.

## Resource Management

**No Connection Limits or Cleanup:**
- Issue: Server accepts unlimited concurrent connections with no max connection limit or per-connection timeout
- Files: `course/server.js` (line 8)
- Impact: Unbounded memory growth; one slow client can hold resources indefinitely
- Risk: Denial of service vulnerability (open unlimited connections and never write data)
- Fix approach: Set `wss.maxConnections` or implement connection counter with upper limit. Add idle timeout to kill inactive connections.

**PTY Process Cleanup Reliability:**
- Issue: PTY processes may not always be killed; `ptyProcess.kill()` is not wrapped in error handling
- Files: `course/server.js` (lines 43, 46)
- Impact: Zombie processes accumulate; resource exhaustion over time
- Recommendation: Use try-catch around `kill()`, verify process is actually terminated, or use `process.kill()` with SIGKILL fallback

**No Memory Limit per Connection:**
- Issue: Large data bursts from clients or PTY output could cause unbounded buffer growth
- Files: `course/server.js`
- Risk: One runaway command (e.g., `yes` or logging loop) could OOM the server
- Fix approach: Set `backpressure` handling on WebSocket writes using `ws.readyState` checks

## Operational Concerns

**Hardcoded Terminal Size:**
- Issue: PTY spawn uses fixed 80x24 terminal size
- Files: `course/server.js` (lines 18-19)
- Impact: Not responsive to client window resize; may cause UI wrapping issues
- Fix approach: Store initial size, handle resize events properly, and allow clients to request size changes

**No Graceful Shutdown:**
- Issue: Server has no shutdown handler; killing the process abruptly closes connections
- Files: `course/server.js`
- Risk: Active terminal sessions are killed without cleanup; browser clients experience abrupt disconnection
- Improvement: Add `process.on('SIGTERM')` handler to close all sockets gracefully before exit

**Minimal Logging for Debugging:**
- Issue: Only connection/disconnection logs exist; no message flow logging or performance metrics
- Files: `course/server.js` (lines 10-12, 15, 42)
- Impact: Difficult to debug issues or understand usage patterns
- Recommendation: Add structured logging with timestamps, connection IDs, and operation types

## Data Flow & Message Handling

**No Message Size Limits:**
- Issue: No validation on incoming message size; JSON.parse on arbitrary data from clients
- Files: `course/server.js` (line 32)
- Risk: Large messages could cause parsing delays or memory exhaustion
- Fix approach: Add `ws.setMaxPayload(limit)` or validate message length before parsing

**No Validation on Resize Parameters:**
- Issue: `parsed.cols` and `parsed.rows` are used directly without bounds checking
- Files: `course/server.js` (lines 35-36)
- Risk: Negative or extremely large values could crash PTY or cause unexpected behavior
- Recommendation: Validate `cols` and `rows` are positive integers within reasonable bounds (e.g., 10-500)

**No Message Type Validation:**
- Issue: Only checks `parsed.type === 'input'` and `parsed.type === 'resize'`; ignores other fields silently
- Files: `course/server.js` (lines 33-37)
- Risk: Unclear behavior for unexpected message types; potential for future bugs if new message types are added without proper handling

## Testing & Quality

**No Tests:**
- Files: `course/server.js`, `course/package.json`
- What's not tested: Connection lifecycle, message handling, error scenarios, cleanup, resource limits
- Risk: Regressions in critical functionality (security, cleanup, error handling) go undetected
- Priority: High
- Recommendation: Add test suite using Node test runner or Jest. Cover: connection lifecycle, malformed messages, PTY spawn failures, process cleanup

**No Documentation:**
- Issue: No README, no inline documentation, no API spec for WebSocket protocol
- Files: Missing `course/README.md`
- Risk: Unclear how to use the server, what the protocol is, how to deploy it safely
- Recommendation: Add README covering setup, security considerations, protocol spec, and limitations

## Dependencies

**Outdated Node-PTY Version:**
- Issue: `node-pty@^1.0.0` is an older major version
- Files: `course/package.json` (line 10)
- Risk: May miss critical security patches or bug fixes in newer versions
- Improvement: Check latest version and upgrade to `^0.10.0` or latest stable (verify semver)

**No Engine Version Specification:**
- Issue: `package.json` doesn't specify Node.js version requirement
- Files: `course/package.json`
- Impact: Could run on incompatible Node versions with unexpected behavior
- Recommendation: Add `"engines": { "node": ">=18.0.0" }` to package.json

## Scaling Limitations

**Single-Process Architecture:**
- Issue: Server runs as single Node.js process; cannot use multiple CPU cores
- Files: `course/server.js`
- Current capacity: Limited by single-threaded Node.js; high client count will cause latency
- Limit: Likely 50-100 concurrent connections before noticeable delays
- Scaling path: Use Node cluster module or PM2 with load balancer frontend

**No Horizontal Scaling:**
- Issue: Each server instance is independent; no session affinity or state sharing
- Risk: Cannot distribute load across multiple servers without stateless redesign
- Solution: Would require WebSocket state store (Redis) and session IDs

## Fragile Areas

**Browser/Server Protocol Contract:**
- Files: `course/server.js`, `course.html`, `index.html`
- Why fragile: JSON message format is implicit; no versioning or validation
- Safe modification: Always validate new message types with tests; document protocol changes; use semantic versioning
- Test coverage: Zero automated tests for protocol; any change to message handling is untested

**PTY Interaction Edge Cases:**
- Files: `course/server.js` (lines 25-48)
- Why fragile: PTY behavior varies by shell and OS; silent error handling masks problems
- Safe modification: Log all PTY state changes; test on target OS; verify process cleanup; handle shell-specific commands carefully

---

*Concerns audit: 2026-03-14*
