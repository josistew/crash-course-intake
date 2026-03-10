# Claude Code Crash Course — YouTube Video Series

**Format:** Free Loom screen recordings, released as chapters on YouTube
**Channel:** Humanity
**Style:** Desktop walkthrough — you talking over your screen, showing real usage
**Target length:** 8-15 min per episode (short enough to finish, long enough to be useful)

---

## Series Structure

### Episode 0: "Install Claude Code in 5 Minutes"
**Type:** Standalone quickstart (this is the hook)
**What you show on screen:**
- Open Terminal
- Run the install command
- Authenticate
- First prompt → first result
- Set up CLAUDE.md

**Why first:** People search "how to install Claude Code" — this is your top-of-funnel. Pin it as the channel trailer.

---

### PART 1 — Claude Code

#### Episode 1: "What Level Are You? (Claude Code Self-Assessment)"
**Maps to:** Chapter 1 — Your Current Level
**What you show:** Walk through the assessment live. "If you already know X, skip to episode 4."
**Goal:** Help people self-sort and know which episodes matter for them.

#### Episode 2: "The Creator's Playbook — 12 Rules for Claude Code"
**Maps to:** Chapter 2 — Boris Cherny's framework
**What you show:** Open a real project. Demonstrate each rule with a live example.
**This is your most shareable episode** — frameworks get shared.

#### Episode 3: "Hooks — Automate Everything Around Claude Code"
**Maps to:** Chapter 3 — Hooks Deep Dive
**What you show:**
- Create a pre-commit hook live
- Show notification hooks
- Permission guardrails
- Before/after of a workflow with and without hooks

#### Episode 4: "MCP Servers — Connect Claude to Everything"
**Maps to:** Chapter 4 — MCP Servers
**What you show:**
- Install an MCP server (Google Sheets, filesystem, etc.)
- Configure it in settings.json
- Use it in a real prompt
- Show the data flowing back

#### Episode 5: "Custom Skills & Slash Commands"
**Maps to:** Chapter 5 — Skills & Slash Commands
**What you show:**
- Create a `/deploy` skill from scratch
- Create a `/morning-report` skill
- Show the skill file structure
- Use them in a real session

#### Episode 6: "Subagents — Run Parallel AI Workers"
**Maps to:** Chapter 6 — Subagents
**What you show:**
- Kick off multiple subagents
- Show them working in parallel
- Real example: refactor + test in parallel

#### Episode 7: "Git Workflows & Background Tasks"
**Maps to:** Chapter 7 — Git & Background Tasks
**What you show:**
- Claude Code managing branches
- Background tasks running while you work
- Real multi-repo workflow

#### Episode 8: "What's New in Claude Code (Latest Updates)"
**Maps to:** Chapter 8 — Recent Updates
**What you show:** Walk through recent changelog. This episode you can re-record quarterly to stay fresh.

---

### PART 2 — Cowork

#### Episode 9: "Claude Cowork — Setup in 5 Minutes"
**Maps to:** Chapter 9 — What Is Cowork & Setup
**What you show:**
- Download and install Cowork
- First session
- Connect Google Drive
- Show the desktop app in action

#### Episode 10: "Cowork Instructions & Plugins"
**Maps to:** Chapter 10 — Instructions & Plugins
**What you show:**
- Write custom instructions
- Enable Finance, Marketing, Operations plugins
- Show plugin output on real data

#### Episode 11: "Cowork Connectors — Wire It Into Your Stack"
**Maps to:** Chapter 11 — Connectors & Use Cases
**What you show:**
- Connect Square POS (or similar)
- Connect Google Workspace
- Run a real business query across connected data

#### Episode 12: "Cowork vs Claude Code — When to Use Which"
**Maps to:** Chapter 12 — Cowork vs Claude Code
**What you show:** Split screen. Same task done in both tools. Show the tradeoffs live.

---

### PART 3 — Power Up

#### Episode 13: "The Power Setup — My Daily Claude Workflow"
**Maps to:** Chapter 13 — Power Setup & Workflow
**What you show:**
- Your actual morning routine with Claude
- Full config walkthrough (CLAUDE.md, hooks, skills, MCP)
- "Here's what my day looks like now"

**This is your closer.** End with a CTA to subscribe and link to the interactive course.

---

## Production Notes

### Recording (Loom)
- **Resolution:** Record at 1920x1080 (YouTube standard)
- **Font size:** Bump terminal font to 16-18px so it's readable on mobile
- **Loom settings:** Enable "Camera bubble" (small circle of your face in corner) — builds trust
- **Clean desktop:** Hide bookmarks bar, close unrelated tabs/apps, use a clean wallpaper
- **Microphone:** Use a decent mic (even AirPods are fine, just not laptop speakers)

### Editing
- Loom has built-in trim/cut — enough for v1
- Add chapter timestamps in YouTube description (viewers love jumping to sections)
- No fancy intros needed. Just "Hey, I'm Josi — this is episode X of the Claude Code crash course"

### YouTube Setup
- **Playlist:** Create a "Claude Code Crash Course" playlist, episodes auto-play in order
- **Thumbnails:** Consistent template — episode number + title + your face or a terminal screenshot
- **Descriptions:** Include timestamps, links to the interactive course, and links to prev/next episodes
- **Tags:** "Claude Code", "Claude AI", "AI coding", "Anthropic", "developer tools", "AI tools"

### Release Strategy
- **Option A — Batch drop:** Record all 14 episodes, release 2-3 per week over ~5 weeks
- **Option B — Rolling release:** Record and release 1-2 per week as you go (lower risk, get feedback early)
- **Recommendation:** Option B. Release Ep 0 (install) + Ep 2 (Creator's Playbook) first — these are the most searchable/shareable. Use early comments to refine the rest.

---

## Companion Resources

Each YouTube episode links back to:
1. **The interactive course** (your GitHub Pages site) — for hands-on exercises
2. **The markdown crash course** — for reference/skimming
3. **Episode-specific CLAUDE.md templates** — downloadable configs viewers can copy

This turns YouTube into the top-of-funnel → interactive course is the deeper experience.

---

## Episode Checklist Template

For each episode before recording:
- [ ] Outline the 3-5 key things you'll show
- [ ] Set up a clean demo project/environment
- [ ] Rehearse once (just talk through it, don't record)
- [ ] Record in Loom (one take is fine — authenticity > polish)
- [ ] Trim dead air at start/end
- [ ] Add to YouTube with timestamps, description, playlist
- [ ] Add YouTube link back to the interactive course chapter
