# Claude Code & Cowork Crash Course — Rez Edition

> Built for a restaurant operator running 5 locations across two brands.
> Tailored to: Square POS, Google Workspace, payroll, marketing, and multi-location reporting.
> Attendees: Rez + Ops Partner
> Last updated: March 3, 2026

---

## Your Current Level

| Capability | Status |
|---|---|
| Terminal / command line | ❌ Never used |
| Coding experience | ❌ None |
| ChatGPT | ✅ Heavy user |
| Claude (web) | ✅ Using — Excel modeling |
| Zapier | ✅ Using for automations |
| Cowork | ⚠️ Light integration — wants deeper |
| Claude Code | ❌ Not installed |
| CLAUDE.md | ❌ Not set up |
| MCP servers | ❌ Not using |
| Agents | ❌ Not using |
| Skills / slash commands | ❌ Not using |

**Your businesses:**
- **Moto Medi** — 3 Mediterranean fast casual locations (Lubbock/Amarillo)
- **Tikka Shack** — Multi-location Indian fast casual franchise

**Your stack:** Square POS, Google Workspace (Sheets, Drive), payroll system, Meta (ads), Google Business Profile, scheduling tools, delivery platforms, custom cost-tracking spreadsheets

**Your pain points:**
1. Manually pulling numbers from Square POS and other dashboards
2. Pulling COGS data weekly by hand
3. Manual payroll reports
4. No automated reporting across 5 locations

**Your #1 goal:** Automate all manual reporting. Payroll is the immediate need.

**Success looks like:** Fully understand what Claude Code and Cowork can do. Walk away with agents built for your business. Have enough knowledge to create and deploy your own solutions going forward.

---

## Part 1: Ground Zero — Your Mac as a Command Center

*You've never opened a terminal. That's fine. This section gets you from zero to dangerous in 30 minutes.*

### 1.1 The Terminal (It's Just a Text Box)

Your Mac has a built-in app called **Terminal**. It's a text-based way to talk to your computer. Instead of clicking buttons, you type commands. That's it.

**Open it:** `Cmd + Space` → type "Terminal" → hit Enter.

You'll see a blinking cursor. This is where you type commands.

**Commands you need to know (and nothing more):**

| Command | What it does | Example |
|---|---|---|
| `ls` | List files in current folder | `ls` |
| `cd` | Change directory (folder) | `cd ~/Desktop` |
| `pwd` | Print where you are | `pwd` |
| `mkdir` | Make a new folder | `mkdir my-project` |
| `open .` | Open current folder in Finder | `open .` |

That's the whole list. You don't need more than this.

**The `~` symbol** means your home folder (`/Users/rez` or whatever your username is).

---

### 1.2 Installing Claude Code

Claude Code runs in the terminal. One command installs it:

```bash
npm install -g @anthropic-ai/claude-code
```

**Wait — what's npm?** It's a package manager. If you don't have it, install Node.js first:

```bash
# Check if you have it
node --version

# If that errors, install Node.js:
# Go to https://nodejs.org → download the LTS version → run the installer
```

Once installed, launch Claude Code:

```bash
claude
```

That's it. You're in. Claude Code is now running in your terminal. You type naturally — just like you do in ChatGPT — but now Claude can actually *do things* on your computer.

---

### 1.3 CLAUDE.md — Teaching Claude About Your Business

This is the single most important concept. A `CLAUDE.md` file is a set of instructions that Claude reads every time you start a session. It's like onboarding a new employee.

**Where it lives:**
- `~/CLAUDE.md` — Global (applies everywhere)
- `~/my-project/CLAUDE.md` — Project-specific (applies only in that folder)

**What to put in yours:**

```markdown
# Rez — Business Context

## Who I Am
Restaurant operator. 5 locations across 2 brands.
- Moto Medi: 3 Mediterranean fast casual locations (Lubbock, Amarillo)
- Tikka Shack: Multi-location Indian fast casual franchise

## My Stack
- Square POS (all locations)
- Google Workspace (Sheets, Drive, Gmail)
- [Your payroll system name]
- Meta Business Suite (ads)
- Google Business Profile (reviews)
- [Scheduling tool name]
- [Delivery platform names]

## How I Work
- I'm not a developer. Explain technical concepts simply.
- I have an ops partner who manages day-to-day at locations.
- We track costs in collaborative Google Sheets with manual inputs.
- Reports are currently built by hand from Square + spreadsheets.

## Key Metrics I Track
- Revenue by location (daily/weekly/monthly)
- COGS by location and category
- Labor cost percentage
- Food cost percentage
- Average ticket size
- Online order volume vs dine-in

## Immediate Priorities
1. Automate payroll reporting
2. Automate COGS data pull
3. Consolidate multi-location reporting into one view
```

**Why this matters:** Every time you open Claude Code or Cowork in a folder with a CLAUDE.md, Claude already knows your business. No re-explaining. No context-setting. Just straight to work.

---

### 1.4 How to Talk to Claude Code

Claude Code isn't a search engine. It's an executor. The way you prompt it changes everything.

**Bad prompt (ChatGPT habits):**
> "Can you help me think about ways to automate my payroll?"

**Good prompt (Claude Code style):**
> "Read my CLAUDE.md for business context. I need you to create a Google Sheet template for weekly payroll reporting across my 5 locations. Columns: employee name, location, hours worked, hourly rate, gross pay, deductions, net pay. Include formulas for totals per location and grand total."

**The difference:** Claude Code *builds things*. Tell it what to build, not what to think about.

**More examples for your business:**

> "Create a weekly P&L template in Google Sheets format with tabs for each of my 5 locations plus a consolidated view. Use the metrics from my CLAUDE.md."

> "Build me a COGS tracking sheet that I can paste Square sales data into and it auto-calculates food cost percentage by category."

> "Draft a Meta ad for Moto Medi promoting our lunch combo. Target 18-45, Lubbock area. Include 3 headline variations and 2 body copy options."

---

## Part 2: Cowork — Your Business Operating System

*You've already dipped into Cowork. This section takes you from dabbling to running your business through it.*

### 2.1 What Cowork Actually Is

Cowork is Claude running on your desktop with the ability to:
- Read and create files on your Mac
- Connect to Google Drive, Gmail, Sheets, and other services
- Browse the web
- Run long tasks while you do other things
- Schedule recurring tasks
- Coordinate multiple workers in parallel

**Think of it as:** A business analyst + operations manager + marketing assistant that works 24/7, understands your entire business, and gets better the more context you give it.

**You already have access** through Claude Max. Open Claude Desktop → click the **Cowork** tab.

---

### 2.2 Connectors — Wiring Claude into Your Tools

Connectors are how Cowork talks to your external services. These are the ones that matter for your business:

| Connector | What it does for you |
|---|---|
| **Google Drive** | Read/write docs, sheets — your cost tracking, reports |
| **Google Sheets** | Direct spreadsheet access — COGS data, payroll, P&Ls |
| **Gmail** | Read and draft emails — vendor communications, team updates |
| **Google Calendar** | Schedule awareness — know what's coming |
| **Web browsing** | Pull data from Square dashboard, Google Business, delivery platforms |

**Setup:** Claude Desktop → Settings → Cowork → Connectors. Toggle on, authenticate with Google.

**Once connected, you can say things like:**
> "Open my COGS tracking sheet in Google Drive and add this week's numbers: [paste data]"

> "Check my Gmail for any invoices from [vendor] this month and summarize the total spend"

> "Go to my Google Business profile for the Amarillo Moto Medi location and summarize the last 30 days of reviews"

---

### 2.3 Plugins — Pre-Built Workflows

Plugins bundle capabilities into roles. Install these:

| Plugin | Why |
|---|---|
| **Finance** | Financial analysis, P&L modeling, cost calculations |
| **Operations** | Process documentation, SOPs, checklists |
| **Marketing** | Content creation, campaign planning, ad copy |
| **Data Analysis** | Spreadsheet formulas, data visualization, reporting |

**How to install:** Cowork → Customize (left sidebar) → Browse Plugins → Install.

**Customize after installing:** Click "Customize" on each plugin to inject your business context. Tell the Finance plugin about your 5 locations. Tell Marketing about your brands.

---

### 2.4 Instructions — Making Cowork Yours

Two levels of instructions (same concept as CLAUDE.md):

**Global Instructions** (Settings → Cowork → Edit Global Instructions):
```
I'm Rez. I own Moto Medi (3 Mediterranean fast casual locations in Lubbock/Amarillo)
and Tikka Shack (multi-location Indian fast casual franchise). All locations use Square POS.

I have zero coding background. Explain everything simply.
My ops partner also uses this — keep outputs clear enough for both of us.

When creating spreadsheets: always include location breakdowns + consolidated totals.
When analyzing costs: food cost % and labor cost % are the two numbers I care about most.

Format everything for quick scanning — bold key numbers, use tables, highlight anything
that needs attention.
```

**Folder Instructions** (auto-created per folder):
- For your finance folder: context about your chart of accounts, vendor list, pay periods
- For your marketing folder: brand voice, target demographics, location-specific details
- For your operations folder: SOPs, checklists, staff procedures

---

### 2.5 Scheduling — Recurring Automation

The `/schedule` command in Cowork sets up tasks that run automatically.

**Examples for your business:**

> "/schedule every Monday at 7am: Pull last week's sales from the COGS tracking sheet, calculate food cost % by location, and create a weekly summary in my Drive"

> "/schedule every Friday at 6pm: Draft a weekend social media post for each Moto Medi location highlighting our most popular dishes this week"

> "/schedule first of month: Create a monthly P&L summary across all 5 locations and email it to me"

This replaces your manual Monday morning number-pulling ritual.

---

### 2.6 Real Prompts for Your Business

**Finance/Reporting:**
> "Here's this week's Square export [paste or attach CSV]. Calculate COGS percentage by location, compare to last week, and flag any location where food cost exceeded 32%."

> "Create a monthly P&L template that I can use for all 5 locations. Include revenue, COGS breakdown (food, paper, beverage), labor, occupancy, and operating expenses. Build in formulas that calculate percentages automatically."

> "Analyze my last 3 months of labor data [paste from payroll]. Tell me which locations are overstaffed on which days based on revenue per labor hour."

**Payroll:**
> "Build a payroll processing checklist for my ops partner. Steps should cover: pulling hours from [scheduling tool], verifying against Square clock-in data, calculating overtime, running the report in [payroll system], and reconciling discrepancies."

> "Here's this pay period's hours [paste data]. Flag anyone over 40 hours, calculate estimated gross pay, and organize by location."

**Marketing/Reviews:**
> "Go to Google Business Profile and summarize the last month of reviews across all Moto Medi locations. Categorize by: food quality, service, speed, cleanliness. Flag any reviews under 3 stars that need a response."

> "Draft Google Business responses for these negative reviews [paste]. Tone: professional, empathetic, solution-oriented. Invite them back."

> "Create a week of Instagram content for Tikka Shack. 3 posts (food shots with captions) + 2 stories (polls, behind-the-scenes). Voice: warm, authentic, flavor-forward."

**Operations:**
> "Build an opening checklist for Moto Medi that covers food prep, equipment checks, POS setup, and front-of-house readiness. Format as a printable single-page PDF."

> "Analyze my delivery platform data [paste]. Which platform has the highest margin after fees? Which menu items perform best on delivery vs dine-in?"

---

## Part 3: Claude Code — The Power Layer

*Claude Code is where you go beyond what Cowork can do alone. It writes code, builds tools, deploys web apps, and connects systems. You don't need to be a developer — Claude does the developing.*

### 3.1 MCP Servers — Giving Claude Superpowers

MCP (Model Context Protocol) servers are plugins that give Claude new abilities. Each server adds tools Claude can use.

**Where they're configured:** `~/.claude/settings.json` (a file in your home folder).

**Servers that matter for your business:**

| Server | What it gives Claude | Your use case |
|---|---|---|
| Google Sheets MCP | Read/write spreadsheets directly | COGS tracking, payroll, P&Ls |
| Google Drive MCP | Read/write documents | Reports, SOPs, templates |
| Web Fetch MCP | Read any web page | Pull data from Square dashboard |
| Filesystem MCP | Access specific folders | Work with your local files |

**How to set one up (we'll do this together):**

```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-google-sheets"],
      "env": {
        "GOOGLE_CLIENT_ID": "<from-google-cloud>",
        "GOOGLE_CLIENT_SECRET": "<from-google-cloud>"
      }
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-fetch"]
    }
  }
}
```

Don't worry about memorizing this. You'll tell Claude Code: *"Set up a Google Sheets MCP server for me"* and it will walk you through it.

---

### 3.2 Skills & Slash Commands — Your Custom Shortcuts

Skills are reusable commands you create. They live as markdown files in `.claude/skills/`.

**Examples built for your business:**

**`/weekly-numbers` — Pull your weekly report:**
```markdown
# /weekly-numbers

Pull weekly performance data across all locations.

## Instructions

1. Read the COGS tracking Google Sheet
2. For each location, calculate:
   - Total revenue
   - Food cost %
   - Labor cost %
   - Average ticket size
3. Compare to the previous week
4. Flag any metric that's off by more than 5%
5. Format as a clean summary table

## Context

- 5 locations: 3 Moto Medi (Lubbock x2, Amarillo), 2+ Tikka Shack
- Target food cost: under 32%
- Target labor cost: under 28%
- Square POS is the source of truth for revenue
```

**`/payroll-prep` — Prep payroll reports:**
```markdown
# /payroll-prep

Prepare payroll data for processing.

## Instructions

1. Read the current pay period's hours from [scheduling tool export / Sheet]
2. Cross-reference with Square clock-in data if available
3. Flag overtime (anyone over 40 hours)
4. Calculate estimated gross pay per employee
5. Organize by location
6. Output a clean summary ready for payroll processing

## Context

- Pay period: [biweekly/weekly]
- 5 locations across 2 brands
- Overtime threshold: 40 hours
```

**`/review-check` — Morning review sweep:**
```markdown
# /review-check

Check Google Business reviews across all locations.

## Instructions

1. Check Google Business Profile for each location
2. Find any new reviews since last check
3. Summarize ratings and sentiment
4. Draft responses for any reviews under 4 stars
5. Flag any recurring complaints

## Context

- 3 Moto Medi locations + Tikka Shack locations
- Response tone: professional, warm, solution-oriented
- Always invite unhappy customers back
```

**To create a skill:** In Claude Code, just say:
> "Create a skill called /weekly-numbers that pulls my weekly performance report"

Claude will create the file for you. You just describe what you want.

---

### 3.3 Agents — Workers That Run in Parallel

When you give Claude a complex task, it can spawn **subagents** — independent workers that handle different pieces simultaneously.

**You don't configure this.** Claude decides when to use subagents automatically. But you can trigger it with how you prompt.

**Single-agent prompt (slow):**
> "Check my reviews, then check my sales, then check my payroll data"

**Multi-agent prompt (fast — 3 agents run simultaneously):**
> "Do these three things at the same time: check Google Business reviews across all my locations, pull this week's sales data from my COGS sheet, and analyze the payroll hours for overtime flags"

Claude spins up 3 workers. Each handles one task. Results come back together.

**Your use case:** Monday morning briefing across all 5 locations — reviews, sales, labor, inventory alerts — all at once instead of one-by-one.

---

### 3.4 Building a Web App (Yes, You)

Claude Code can build, deploy, and host web applications. You describe what you want. Claude writes the code, tests it, and deploys it.

**Why this matters for you:** Instead of paying for expensive SaaS dashboards, you can have Claude build exactly what you need.

**Example — Multi-Location Dashboard:**
> "Build me a web dashboard that reads from my Google Sheet and shows:
> - Revenue by location (bar chart)
> - Food cost % trend over the last 8 weeks (line chart)
> - Labor cost % by location (gauge charts)
> - A table of this week's numbers vs last week
> Make it mobile-friendly so I can check it from my phone.
> Use a dark theme with clean typography."

Claude Code will:
1. Create the project
2. Write all the code (Next.js, React, whatever it decides is best)
3. Connect it to your Google Sheet
4. Deploy it to Vercel (free hosting)
5. Give you a URL you can bookmark on your phone

**That's a real, live web app.** Built in one session. Updated automatically when your Sheet updates.

---

## Part 4: Live Builds — What We'll Create Together

*You said you want to build 1-2 deployable things and walk away with a full understanding. Here's what we're building.*

### Build 1: Payroll Automation System

**The problem:** You manually pull hours, cross-reference data, calculate overtime, and prep payroll reports. Across 5 locations, this eats hours every pay period.

**What we'll build:**
1. A Google Sheet template structured for multi-location payroll
2. A Claude Code skill (`/payroll-prep`) that processes raw hours data
3. Automated calculations: overtime flagging, gross pay estimates, location breakdowns
4. A Cowork scheduled task that preps the data before each pay period

**You'll walk away with:**
- A repeatable payroll prep workflow that takes minutes instead of hours
- A skill you can run anytime with one command
- Understanding of how to modify it as your needs change

---

### Build 2: Multi-Location Performance Dashboard

**The problem:** You manually pull numbers from Square, spreadsheets, and other dashboards to understand how your locations are performing. No single view.

**What we'll build:**
1. A consolidated Google Sheet that acts as your data hub
2. A live web dashboard that reads from that Sheet
3. Location-by-location metrics: revenue, COGS, labor, trends
4. Mobile-friendly — check it from your phone between location visits
5. Auto-updating — new data in the Sheet means new data on the dashboard

**You'll walk away with:**
- A deployed dashboard at a URL you own
- Understanding of how Claude Code builds and deploys web apps
- The ability to ask Claude to add features later (new charts, new metrics, alerts)

---

## Part 5: Power Setup — Your Daily System

### 5.1 Your Recommended Configuration

**Cowork (primary daily tool):**
1. Global instructions set with your business context
2. Finance + Operations + Marketing plugins installed and customized
3. Google Drive + Gmail + Sheets connectors active
4. Folder instructions for finance, marketing, operations
5. Scheduled tasks: weekly numbers pull, monthly P&L, review monitoring

**Claude Code (power tool for building):**
1. CLAUDE.md with full business context
2. MCP servers: Google Sheets, web fetch
3. Custom skills: `/weekly-numbers`, `/payroll-prep`, `/review-check`
4. Dashboard project deployed on Vercel

**How they work together:**
- **Cowork** handles daily knowledge work — reports, drafts, analysis, emails, reviews
- **Claude Code** builds the tools and systems that Cowork uses — dashboards, automations, templates

---

### 5.2 Daily Workflow

**Morning (5 min — Cowork):**
> "Morning briefing: Check reviews across all locations, pull yesterday's sales numbers, flag anything that needs my attention."

Cowork runs multiple agents, checks your Google Sheets, scans Google Business, and gives you a single summary to skim before you leave for the first location.

**During the week (as needed — Cowork):**
- Draft vendor emails
- Create social media content
- Analyze delivery platform performance
- Prep for meetings with ops partner
- Process new employee paperwork

**Pay period (Claude Code):**
> "/payroll-prep"

One command. Payroll data pulled, overtime flagged, location breakdowns generated.

**End of month (Cowork):**
> "Create the monthly P&L for all 5 locations. Compare to last month. Highlight the top 3 areas where we're trending in the wrong direction."

**When you need something new (Claude Code):**
> "Add an inventory tracking page to my dashboard that shows theoretical vs actual food cost by location"

You describe it. Claude builds it. Deploys it. Done.

---

### 5.3 From Zapier to Claude — What Changes

You're already using Zapier for automations. Here's how Claude fits in:

| Zapier | Claude |
|---|---|
| Trigger → Action (rigid) | Natural language (flexible) |
| Per-zap pricing | Included in your Max subscription |
| Can't analyze data, just move it | Analyzes, summarizes, decides, then acts |
| Separate tool to manage | Lives in your daily workflow |
| Pre-built integrations only | Claude can build custom integrations |

**You don't have to ditch Zapier immediately.** Keep what's working. But for anything that requires thinking (not just moving data from A to B), Claude is the play.

---

### 5.4 Teaching Your Ops Partner

Your ops partner is attending this crash course. Here's how to split responsibilities:

**Ops partner focuses on:**
- Cowork for daily operations (checklists, vendor comms, scheduling)
- Running skills like `/weekly-numbers` and `/payroll-prep`
- Checking the dashboard on their phone
- Using Cowork for review responses and social content

**You focus on:**
- Building new skills and systems in Claude Code
- Deploying and updating the dashboard
- Setting up new automations as needs arise
- Strategic analysis and planning with Cowork

Both of you can use the same CLAUDE.md and skills. Both of you can run Claude Code. The difference is just focus.

---

## Quick Reference

### Terminal Commands (The Only Ones You Need)

| Command | What it does |
|---|---|
| `claude` | Start Claude Code |
| `ls` | List files |
| `cd ~/folder` | Go to a folder |
| `pwd` | Where am I? |
| `open .` | Open folder in Finder |

### Cowork Essentials

| Action | How |
|---|---|
| Start Cowork | Claude Desktop → Cowork tab |
| Set instructions | Settings → Cowork → Edit Global Instructions |
| Add connector | Settings → Cowork → Connectors |
| Install plugin | Customize → Browse Plugins |
| Schedule task | `/schedule` command in Cowork |

### Claude Code Essentials

| Action | How |
|---|---|
| Create a CLAUDE.md | Tell Claude: "Create a CLAUDE.md for this project" |
| Create a skill | Tell Claude: "Create a skill called /name that does X" |
| Add MCP server | Tell Claude: "Set up a Google Sheets MCP server" |
| Run a skill | Type `/skillname` in Claude Code |
| Build a web app | Describe what you want. Claude builds it. |
| Deploy | Tell Claude: "Deploy this to Vercel" |

### Custom Skills for Your Business

| Skill | What it does |
|---|---|
| `/weekly-numbers` | Pulls weekly performance across all 5 locations |
| `/payroll-prep` | Preps payroll data for processing |
| `/review-check` | Scans Google Business reviews, drafts responses |
| `/cogs-report` | Calculates food cost % by location from Square data |
| `/morning` | Full morning briefing — reviews + sales + alerts |

---

*This course is built for two restaurant operators who want to stop pulling numbers by hand and start running their business through AI. Everything here is specific to your stack, your locations, and your actual daily work.*
