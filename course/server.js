const { WebSocketServer } = require('ws');
const pty = require('node-pty');
const os = require('os');

const PORT = 8767;
const shell = os.platform() === 'win32' ? 'powershell.exe' : process.env.SHELL || 'zsh';

const wss = new WebSocketServer({ port: PORT });

console.log(`\x1b[32m✓\x1b[0m Terminal server running on ws://localhost:${PORT}`);
console.log(`\x1b[90m  Open the crash course in your browser to connect.\x1b[0m`);
console.log(`\x1b[90m  Press Ctrl+C to stop.\x1b[0m\n`);

wss.on('connection', (ws) => {
  console.log('\x1b[32m✓\x1b[0m Browser connected');

  const ptyProcess = pty.spawn(shell, [], {
    name: 'xterm-256color',
    cols: 80,
    rows: 24,
    cwd: os.homedir(),
    env: { ...process.env, TERM: 'xterm-256color' },
  });

  ptyProcess.onData((data) => {
    try { ws.send(JSON.stringify({ type: 'output', data })); }
    catch (e) { /* ws closed */ }
  });

  ws.on('message', (msg) => {
    try {
      const parsed = JSON.parse(msg);
      if (parsed.type === 'input') {
        ptyProcess.write(parsed.data);
      } else if (parsed.type === 'resize') {
        ptyProcess.resize(parsed.cols, parsed.rows);
      }
    } catch (e) { /* ignore malformed */ }
  });

  ws.on('close', () => {
    console.log('\x1b[33m○\x1b[0m Browser disconnected');
    ptyProcess.kill();
  });

  ptyProcess.onExit(() => {
    try { ws.close(); } catch (e) { /* already closed */ }
  });
});
