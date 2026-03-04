# Claude Code & Cowork Crash Course — Josi Edition

> Built around what you already know and what you're missing.
> Last updated: March 3, 2026

---

## Your Current Level

| Feature | Status |
|---|---|
| CLAUDE.md | ✅ Strong |
| Auto-memory / /memory | ✅ Using regularly |
| Skills / slash commands | ⚠️ Using some, wants more |
| Hooks | ⚠️ Surface level |
| MCP servers | ⚠️ Surface level |
| Subagents | ❌ Not using |
| Git workflows | ❌ Not using |
| Background tasks | ❌ Not using |
| Cowork | ❌ Never used |

---

## Part 1: Claude Code — What You're Missing

### 1.1 Hooks (Deep Dive)

Hooks are commands that run automatically at specific points in Claude's workflow. You configure them in `.claude/settings.json`. Think of them as "if Claude does X, also do Y."

**Four hook types:**
- **Command hooks** — Run a shell command (formatting, linting, logging)
- **HTTP hooks** — POST JSON to a URL (send notifications, trigger webhooks)
- **Prompt hooks** — Ask an LLM a yes/no question (smart gatekeeping)
- **Agent hooks** — Spawn a subagent to verify complex conditions

**Five hook events:**
| Event | When it fires |
|---|---|
| `PreToolUse` | Before Claude runs any tool (block dangerous commands) |
| `PostToolUse` | After a tool completes (auto-format files, log actions) |
| `PostToolUseFailure` | When a tool fails (custom error handling) |
| `PermissionRequest` | When Claude asks for permission (auto-approve safe patterns) |
| `Notification` | When Claude sends a notification (forward to Slack, Telegram) |

**Example — Auto-format on every file write:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "type": "command",
        "command": "prettier --write $CLAUDE_FILE_PATH"
      }
    ]
  }
}
```

**Example — Send Telegram notification when Claude finishes a task:**
```json
{
  "hooks": {
    "Notification": [
      {
        "type": "http",
        "url": "https://api.telegram.org/bot<TOKEN>/sendMessage",
        "method": "POST",
        "body": {
          "chat_id": "<YOUR_CHAT_ID>",
          "text": "Claude finished: $CLAUDE_NOTIFICATION"
        }
      }
    ]
  }
}
```

**Example — Block destructive git commands:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "type": "prompt",
        "prompt": "Is this command destructive (force push, reset --hard, rm -rf)? Answer YES to block, NO to allow."
      }
    ]
  }
}
```

**Your opportunity:** You run Moltbot agents on your Mac Mini. Hooks could auto-notify you via Telegram (Bean/Egg) when Claude Code finishes long tasks, auto-lint code, or auto-commit after successful builds.

---

### 1.2 MCP Servers (Deep Dive)

MCP (Model Context Protocol) lets Claude connect to external tools and data sources. Each MCP server exposes "tools" that Claude can call like native capabilities.

**Where MCP configs live:**
- **Global:** `~/.claude/settings.json` (available in all projects)
- **Project:** `.claude/settings.json` (project-specific, committed to git)
- **Local:** `.claude/settings.local.json` (project-specific, NOT committed — good for secrets)

**Config structure:**
```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/folder"],
      "env": {}
    }
  }
}
```

**MCP servers you should know about:**

| Server | What it does | Why you'd use it |
|---|---|---|
| `@anthropic/claude-code-mcp` | Exposes Claude Code itself as an MCP tool | Let Cowork or other Claude instances call Claude Code |
| `@modelcontextprotocol/server-filesystem` | Read/write files in specified directories | Give Claude access to specific folders |
| `@modelcontextprotocol/server-github` | GitHub API (issues, PRs, repos) | Manage repos without leaving Claude |
| `@anthropic/mcp-server-fetch` | Fetch web pages | Let Claude read URLs |
| Google Sheets MCP | Read/write Google Sheets | Your LeaseJenny dashboard, lead tracking |
| Slack MCP | Send/read Slack messages | Notifications, team updates |

**MCP tools in hooks:** MCP tools follow the pattern `mcp__<server>__<tool>`. You can write hooks that trigger on specific MCP tools:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "mcp__github__.*",
        "type": "command",
        "command": "echo 'GitHub action taken' >> ~/claude-audit.log"
      }
    ]
  }
}
```

**Your opportunity:** Connect Google Sheets MCP for LeaseJenny lead data. Connect GitHub MCP for your repos. Set up a filesystem MCP so Cowork can access your project files.

---

### 1.3 Skills & Slash Commands (Going Deeper)

You use some skills already but want more. Here's the full picture.

**Built-in skills you might not know about:**
- `/simplify` — Reviews changed code for reuse, quality, efficiency, then fixes issues
- `/batch` — Run the same operation across multiple files
- `/copy` — Interactive picker to copy specific code blocks (NEW)
- `/memory` — View and manage auto-memory files
- `/model` — Switch models mid-conversation (now shows current model)
- `/voice` — Voice input mode (NEW, rolling out gradually)

**Custom skills** live in `.claude/skills/` as markdown files. Each file becomes a slash command.

**Skill file structure:**
```markdown
# /my-skill-name

Description of what this skill does.

## Instructions

Step-by-step instructions Claude follows when this skill is invoked.

## Context

Any context Claude needs (file paths, conventions, etc.)
```

**Example — `/deploy` skill for your projects:**
```markdown
# /deploy

Deploy the current project to Vercel.

## Instructions

1. Run the build command to verify no errors
2. Check git status — commit any uncommitted changes first
3. Run `vercel --prod` to deploy
4. Report the deployment URL when done

## Context

- Always use `--prod` flag for production deploys
- If build fails, fix the issue before deploying
```

**Example — `/morning-report` skill for LeaseJenny:**
```markdown
# /morning-report

Generate a morning leads report.

## Instructions

1. Read the Google Sheet for LeaseJenny leads
2. Count new leads from the last 24 hours
3. Summarize qualification status (qualified vs disqualified)
4. List any leads that need follow-up
5. Format as a clean summary I can skim in 30 seconds
```

**Your opportunity:** Build skills for your recurring workflows — deploying projects, checking lead status, generating reports, auditing your Moltbot agents.

---

### 1.4 Subagents (The Feature You're Not Using)

Subagents let Claude spawn independent workers that run in parallel. This is one of the most powerful features you're not touching.

**When to use subagents:**
- Researching multiple things at once (search 3 codebases simultaneously)
- Running independent tasks that don't depend on each other
- Protecting your main context window from getting bloated with search results
- Exploring a codebase deeply without losing your place

**How they work:** Claude automatically uses the `Agent` tool to spawn subagents. You can also configure agent types in your CLAUDE.md or skills.

**Built-in agent types:**
| Type | Purpose |
|---|---|
| `Explore` | Fast codebase exploration — find files, search code, answer questions |
| `Plan` | Architecture planning — design implementation strategies |
| `general-purpose` | Research, search, multi-step tasks |

**Example prompt that triggers subagents:**
> "Research how Square's API handles webhook notifications, AND check my LeaseJenny codebase for any existing webhook handlers, AND find examples of Square webhook implementations on GitHub"

Claude will spawn 3 parallel agents instead of doing these sequentially.

**Your opportunity:** When working on multi-project tasks (LeaseJenny + stock screener + Humanity), subagents let you research across all of them simultaneously.

---

### 1.5 Git Workflows

Claude Code is excellent at git operations you're probably doing manually:

- **Commits:** `/commit` — Analyzes changes, writes message, commits
- **PRs:** "Create a PR for this branch" — Pushes, writes title/description, creates PR via `gh`
- **Branch management:** "Create a feature branch for the new dashboard"
- **Diff review:** "What changed since yesterday?"
- **Conflict resolution:** "Resolve the merge conflicts in this file"

**Your opportunity:** You have multiple GitHub repos (leasejenny-dashboard, crash-course-intake, etc.). Let Claude handle the git ceremony.

---

### 1.6 Background Tasks

Run long commands without blocking your conversation:

```
"Run the build in the background and let me know when it finishes"
"Deploy to Vercel in the background while I keep working"
```

Claude uses `run_in_background` on Bash commands and notifies you when they complete. You can keep working on other things in the same session.

**Your opportunity:** Deploy one project while working on another. Run tests in the background. Build in the background while writing new code.

---

### 1.7 Recent Updates You Might Have Missed

| Feature | What's new |
|---|---|
| **Auto-memory** | Now auto-saves useful context without you asking. Manage with `/memory` |
| **`/copy` picker** | Interactive selector — pick specific code blocks, not just full response |
| **`/simplify`** | Reviews and simplifies changed code automatically |
| **`/batch`** | Same operation across multiple files at once |
| **HTTP hooks** | POST JSON to URLs (webhooks, APIs) — not just shell commands |
| **Voice mode** | `/voice` — speak your commands (rolling out gradually) |
| **Worktree sharing** | Auto-memory and project configs now shared across git worktrees |
| **Smarter bash prefixes** | "Always allow" now works per-subcommand in piped commands |

---

## Part 2: Claude Cowork — From Zero

### 2.1 What Is Cowork?

Cowork is Claude Code's power applied to knowledge work — not just coding. It runs in the Claude Desktop app (you have Max, so you have access).

**The shift:** Instead of chatting back and forth, you describe an outcome, Claude plans it, executes it, and you come back to finished work. It's like leaving a task for a coworker.

**What it can do:**
- Read, edit, and create files on your computer
- Generate polished deliverables (spreadsheets with formulas, presentations, reports)
- Browse the web (with Claude in Chrome extension)
- Connect to external tools (Google Drive, Gmail, Slack, etc.)
- Run long tasks while you step away
- Coordinate multiple sub-agents in parallel
- Schedule recurring tasks with `/schedule`

---

### 2.2 Setup (5 Minutes)

1. Open **Claude Desktop** (make sure it's updated)
2. Click the **"Cowork"** tab in the mode selector (next to "Chat")
3. You're in. That's it.

**Give it folder access:**
- When you start a task involving files, Cowork will ask which folder to access
- Grant access to specific folders (e.g., `~/LeaseJenny`, `~/humanity-brand`)
- Claude can only see what you explicitly allow

---

### 2.3 Instructions (Your Cowork CLAUDE.md)

Two levels, just like Claude Code:

**Global Instructions** (apply to every session):
- Settings > Cowork > Edit Global Instructions
- Put your role, tone, formatting preferences here

Example:
```
I'm Josiah Stewart. I run Reside Rentals (property management) and Humanity AI (AI agents for businesses).

I prefer direct, concise communication. No fluff.
Format outputs for quick scanning — bullets, headers, bold key info.
When creating files, follow the aesthetics guide in my CLAUDE.md.
Ask before making irreversible changes.
```

**Folder Instructions** (activate when working in a specific folder):
- Created automatically or manually in each folder
- Great for project-specific context

Example for `~/LeaseJenny/`:
```
This is LeaseJenny — AI-powered lead qualification for FB Marketplace rental listings.
Stack: Next.js, Tailwind, Google Sheets API, GoHighLevel.
Two properties: 2416 31st St Lubbock, 516 7th St Wolfforth.
See config files in /config/ for per-listing details.
```

---

### 2.4 Plugins

Plugins bundle skills + connectors + slash commands into packages for specific roles.

**How to install:**
1. In Cowork, click **"Customize"** in the left sidebar
2. Click **"Browse plugins"**
3. Click **"Install"** on what you want

**Plugins relevant to you:**
- **Marketing** — Content creation, campaign planning
- **Sales** — Lead management, outreach
- **Finance** — Financial analysis, reporting
- **Operations** — Process optimization, documentation
- **Data Analysis** — Spreadsheet work, data visualization
- **Plugin Create** — Build your own custom plugins

**Customize after installing:** Click "Customize" on any installed plugin to swap connectors, add your business context, and adjust workflows to match how you actually work.

---

### 2.5 Connectors

Connectors link Cowork to external services. These are MCP servers under the hood.

**Built-in connectors include:**
- Google Drive (read/write docs, sheets)
- Gmail (read/send emails)
- Slack (messages, channels)
- GitHub (repos, issues, PRs)
- Web browsing (via Claude in Chrome)

**Setup:** Settings > Cowork > Connectors. Toggle on what you need and authenticate.

---

### 2.6 Real Use Cases for Your Business

**LeaseJenny:**
- "Go through the LeaseJenny leads sheet, identify qualified leads from the last week, and draft follow-up messages for each one"
- "Create a weekly landlord report summarizing new inquiries, qualified leads, and showing trends"

**Humanity AI:**
- "Read the brand strategy doc and create a one-page sales sheet for dental offices"
- "Draft 5 LinkedIn posts about AI for small business based on my brand voice"
- "Take the ad performance data and build a report with recommendations"

**Stock Screener:**
- "Analyze my last 2 weeks of trades, calculate win rate, average gain/loss, and suggest parameter tweaks"
- "Create a daily performance spreadsheet template with the formulas built in"

**General:**
- "Organize my Downloads folder — sort by type, rename with dates, delete duplicates"
- "Read all my CLAUDE.md files across projects and create a master inventory of what I'm working on"
- "Schedule a daily 8am task: check LeaseJenny leads sheet and send me a summary via email"

---

### 2.7 Cowork vs Claude Code — When to Use Which

| Scenario | Use |
|---|---|
| Writing code, debugging, deploying | **Claude Code** (terminal) |
| Creating documents, spreadsheets, presentations | **Cowork** (desktop) |
| Working within a git repo | **Claude Code** |
| Working with files outside of code projects | **Cowork** |
| Need terminal/shell access | **Claude Code** |
| Need Google Drive / Gmail / Slack integration | **Cowork** |
| Quick coding task | **Claude Code** |
| Multi-step knowledge work (research → draft → format → deliver) | **Cowork** |
| Building and running MCP servers | **Claude Code** |
| Using pre-built plugins for business workflows | **Cowork** |

They share the same foundation. Think of Claude Code as the dev tool and Cowork as the business tool.

---

## Part 3: Putting It Together — Your Power Setup

### 3.1 Recommended Configuration

**Claude Code (`~/.claude/settings.json`):**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "<your-token>" }
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-fetch"]
    }
  },
  "hooks": {
    "Notification": [
      {
        "type": "command",
        "command": "osascript -e 'display notification \"$CLAUDE_NOTIFICATION\" with title \"Claude Code\"'"
      }
    ]
  }
}
```

**Custom skills to build:**
1. `/deploy` — Deploy any project to Vercel
2. `/leads` — Check LeaseJenny leads status
3. `/trades` — Check stock screener performance
4. `/morning` — Morning briefing across all projects

**Cowork setup:**
1. Install Marketing, Sales, and Operations plugins
2. Connect Google Drive + Gmail
3. Set global instructions with your business context
4. Set folder instructions for LeaseJenny, Humanity, stock-screener

### 3.2 Daily Workflow

**Morning (Cowork):**
- Open Cowork, run "morning briefing" — checks leads, trades, emails
- Review and act on what matters

**During the day (Claude Code):**
- Build features, fix bugs, deploy
- Use subagents for cross-project research
- Background tasks for builds/deploys

**End of day (Cowork):**
- "Summarize what I worked on today"
- "Draft any follow-up emails needed"
- "Schedule tomorrow's tasks"

---

## Quick Reference

| Command | What it does |
|---|---|
| `/memory` | View/manage auto-memory |
| `/copy` | Pick specific code blocks to copy |
| `/simplify` | Review & simplify changed code |
| `/batch` | Same operation across multiple files |
| `/voice` | Voice input mode |
| `/model` | Switch models mid-session |
| `/commit` | Smart git commit |
| `/clear` | Reset context |

---

*This course is tailored to your stack and workflow. Work through it section by section, or jump to whatever's most useful.*
