# Phase 3: Daily Checklist App - Research

**Researched:** 2026-03-14
**Domain:** Next.js 15 / Google Sheets API / tablet-optimized UI / append-only writes
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Categories: opening procedures, closing procedures, cleaning/sanitation, equipment checks
- Shift types: Opening and Closing
- Staff flow: tap location → tap shift → enter name → see checklist → tap items to complete
- No login/password — name entry only (shared tablet, minimal friction)
- Optional notes field on any item
- Automatic timestamp on completion
- Google Sheets as data store (service account, same pattern as LeaseJenny)
- Completions log: staff name, location, shift, item, timestamp
- Shared tablet at each store (confirmed by Rez)
- Tablet-optimized: large tap targets, no pinch-zoom
- Bookmarked URL on each store's tablet
- Manager dashboard: all-location completion view for today, reads from Sheets completions log
- No data entry from managers — read only
- Shows: which shifts complete, in progress, not started
- 5 locations: Moto Medi Lubbock 1, Moto Medi Lubbock 2, Moto Medi Amarillo, Tikka Shack 1, Tikka Shack 2
- Separate standalone Next.js project (not in crash-course-intake repo)
- Separate Google Sheet (never references the Reporting Sheet)
- New Vercel deployment

### Claude's Discretion
- Specific UI design, color scheme, animations
- Checklist item organization within categories
- How manager dashboard aggregates/displays data
- Whether checklist items are hardcoded or configurable via Sheet

### Deferred Ideas (OUT OF SCOPE)
- Completion trend analysis over time per location (v2)
- Shift handoff notes visible to next shift (v2)
- Photo attachment for equipment issues (v2)
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| CHK-01 | Staff can select their location and shift type (Opening/Closing) on a tablet-friendly interface | App Router page with large-button location/shift selector; session stored in React state |
| CHK-02 | Staff can enter their name at shift start (no password/login required) | Simple text input on session-start screen; name persists in component state for the session |
| CHK-03 | Checklist displays categorized items: opening procedures, closing procedures, cleaning/sanitation, equipment checks | Hardcoded or Sheet-driven checklist config; filtered by location + shift; grouped by category |
| CHK-04 | Staff can tap items to mark complete with automatic timestamp capture | Client-side optimistic toggle + Server Action to append completion row; `new Date().toISOString()` for timestamp |
| CHK-05 | Staff can add optional notes to any checklist item (e.g., "ice machine not working") | Expandable notes input per item; notes column included in Completions-Log append row |
| CHK-06 | Completion data writes to Google Sheets (who completed, when, which location, which items) | `spreadsheets.values.append` via Server Action; service account auth; exponential backoff on 429 |
| CHK-07 | Manager dashboard shows today's checklist completion status across all locations | `/dashboard` route reads Manager-View tab (QUERY pre-computed in Sheet); no auth needed for v1 |
| CHK-08 | Checklist app deployed to Vercel and accessible via bookmarked URL on store tablets | Standard `next build` + Vercel deploy; env vars for service account + sheet ID |
| CHK-09 | Tablet-optimized UI with large tap targets, no pinch-zoom required | `minimum-scale=1, maximum-scale=1` viewport meta; min 56px touch targets; Tailwind touch utilities |
</phase_requirements>

---

## Summary

Phase 3 is the only phase in the Rez Operations Suite that requires code. It is a standalone Next.js 16 app (matching the existing LeaseJenny pattern) deployed to Vercel, writing checklist completions to a dedicated Google Sheet via a service account. The entire auth, data-fetching, and write pattern is proven and working in the existing LeaseJenny dashboard at `/Users/josi/leasejenny-dashboard/` — this is not exploratory territory.

The primary technical concern is concurrent write safety: multiple staff at the same location tapping simultaneously could lose writes if not handled. Research confirms `spreadsheets.values.append` is atomic for single rows but is not serialized across concurrent callers — two simultaneous appends can collide. For a shared-tablet-per-location scenario (one device per store), true simultaneous writes from the same location are extremely unlikely, so append-only + exponential backoff on HTTP 429 is sufficient without a write buffer. The "ghost session" problem (prior shift's partial checklist lingering on the tablet) is a real UX risk and must be explicitly addressed at session-start via a clear location + shift selection that resets all state.

The manager dashboard should read from a Manager-View tab that contains pre-computed QUERY formulas in the Sheet, matching the architecture decision already documented. The Next.js route simply fetches that computed tab — it does not aggregate in code.

**Primary recommendation:** Build exactly like LeaseJenny (googleapis service account, Server Actions for writes, API routes for reads), add tablet-specific viewport and touch CSS, use append-only Sheets writes with exponential backoff, and invest UI effort in a session-start screen that makes location/shift selection unmistakably clear before the checklist renders.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| next | 16.1.6 | App framework | Matches LeaseJenny exactly; App Router Server Actions keep credentials server-side |
| react / react-dom | 19.2.3 | UI runtime | Matches LeaseJenny exactly |
| googleapis | ^171.4.0 | Google Sheets API client | Official Google client; already used in LeaseJenny; service account auth built in |
| tailwindcss | ^4 | Styling | v4 required for Next.js 15+ Turbopack — v3 has documented `fs` resolution bug with Turbopack |
| @tailwindcss/postcss | ^4 | PostCSS integration | Required with Tailwind v4 |
| typescript | ^5 | Type safety | Consistent with LeaseJenny |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| google-spreadsheet | 5.2.0 | Higher-level Sheets wrapper | Optional; use if raw googleapis calls become verbose for multi-tab reads; LeaseJenny uses raw googleapis and that is fine |

### Alternatives NOT to Use

| Instead of | Could Use | Why NOT |
|------------|-----------|---------|
| Tailwind v4 | Tailwind v3 | v3 has documented `fs` resolution bug with Turbopack in Next.js 15+ |
| googleapis direct | next-auth / auth.js | No auth needed for this app; unnecessary complexity |
| Server Actions | third-party form libs | Server Actions are native to App Router; no additional dep needed |
| Hardcoded checklist | Sheet-driven checklist config | Hardcoded is simpler for v1; Sheet-driven is v2 if Rez wants to edit items himself |
| Vercel KV write buffer | Direct Sheets append | KV adds operational complexity; single tablet per location makes true simultaneous writes improbable |

**Installation (matches LeaseJenny):**
```bash
npx create-next-app@latest checklist-app --typescript --tailwind --app --src-dir
cd checklist-app
npm install googleapis
```

---

## Architecture Patterns

### Google Sheet Structure

Three tabs in a dedicated Checklist Sheet (separate from the Reporting Sheet):

```
Checklist-Template tab:
  Row 1: Headers — Location, Shift, Category, ItemID, ItemText, SortOrder
  Row 2+: One row per checklist item
  Used by: (v1) hardcoded in code, NOT read from Sheet
           (v2 at Claude's discretion) read via API on session start

Completions-Log tab:
  Row 1: Headers — Timestamp, Location, Shift, StaffName, ItemID, ItemText, Category, Notes
  Row 2+: One row per completion event (append-only, never updated in place)
  Written by: Server Action via spreadsheets.values.append

Manager-View tab:
  QUERY formula pre-aggregates today's completions by location/shift
  Read by: /dashboard API route
  Never written to by the app — Sheet formula only
```

### Recommended Project Structure

```
src/
├── app/
│   ├── layout.tsx          # viewport meta — no pinch-zoom
│   ├── page.tsx            # session start: location + shift selector
│   ├── checklist/
│   │   └── page.tsx        # checklist UI — requires location/shift/name in state
│   ├── dashboard/
│   │   └── page.tsx        # manager dashboard — reads Manager-View tab
│   └── api/
│       ├── checklist/route.ts     # GET: fetch checklist items for location+shift
│       └── dashboard/route.ts    # GET: fetch Manager-View tab data
├── lib/
│   ├── sheets.ts           # auth + read helpers (mirrors LeaseJenny pattern)
│   └── checklist-config.ts # hardcoded checklist items per location/shift/category
├── actions/
│   └── completions.ts      # Server Action: appendCompletion()
└── components/
    ├── LocationShiftSelector.tsx
    ├── NameEntry.tsx
    ├── ChecklistItem.tsx
    ├── ChecklistCategory.tsx
    └── ManagerDashboard.tsx
```

### Pattern 1: Service Account Auth (exact LeaseJenny pattern)

**What:** Service account credentials stored base64-encoded in Vercel env var, decoded at runtime, never exposed client-side.

**When to use:** All Sheets API calls — both reads and writes.

```typescript
// Source: /Users/josi/leasejenny-dashboard/src/lib/sheets.ts (proven pattern)
import { google } from 'googleapis';

function getAuth() {
  const keyBase64 = process.env.GOOGLE_SERVICE_ACCOUNT_KEY;
  if (!keyBase64) throw new Error('GOOGLE_SERVICE_ACCOUNT_KEY is not set');
  const keyJson = JSON.parse(Buffer.from(keyBase64, 'base64').toString('utf-8'));
  return new google.auth.GoogleAuth({
    credentials: keyJson,
    scopes: ['https://www.googleapis.com/auth/spreadsheets'],  // note: readwrite scope for checklist app
  });
}
```

**Critical difference from LeaseJenny:** LeaseJenny uses `spreadsheets.readonly` scope. The checklist app needs write access — use `https://www.googleapis.com/auth/spreadsheets` (read/write).

### Pattern 2: Append-Only Write via Server Action

**What:** Server Action receives a completion event and appends one row to Completions-Log. Never updates existing rows. Includes exponential backoff for 429 errors.

**When to use:** Every time staff taps a checklist item to mark complete.

```typescript
// src/actions/completions.ts
'use server';

import { google } from 'googleapis';

function getAuth() { /* same as above */ }

export async function appendCompletion(params: {
  location: string;
  shift: 'Opening' | 'Closing';
  staffName: string;
  itemId: string;
  itemText: string;
  category: string;
  notes: string;
}) {
  const auth = getAuth();
  const sheets = google.sheets({ version: 'v4', auth });
  const sheetId = process.env.CHECKLIST_SHEET_ID;
  if (!sheetId) throw new Error('CHECKLIST_SHEET_ID is not set');

  const timestamp = new Date().toISOString();
  const row = [
    timestamp,
    params.location,
    params.shift,
    params.staffName,
    params.itemId,
    params.itemText,
    params.category,
    params.notes,
  ];

  // Exponential backoff on 429
  let attempt = 0;
  while (attempt < 4) {
    try {
      await sheets.spreadsheets.values.append({
        spreadsheetId: sheetId,
        range: "'Completions-Log'!A:H",
        valueInputOption: 'USER_ENTERED',
        insertDataOption: 'INSERT_ROWS',
        requestBody: { values: [row] },
      });
      return { success: true, timestamp };
    } catch (err: any) {
      if (err?.code === 429 && attempt < 3) {
        await new Promise(r => setTimeout(r, Math.pow(2, attempt) * 500));
        attempt++;
      } else {
        throw err;
      }
    }
  }
}
```

### Pattern 3: Optimistic UI for Checklist Taps

**What:** Mark item complete immediately in client state; fire Server Action in background. If action fails, revert and show error.

**When to use:** All checklist item toggles. Restaurant environments have spotty WiFi — perceived instant feedback is critical.

```typescript
// ChecklistItem.tsx pattern
const [completed, setCompleted] = useState(false);
const [pending, setPending] = useState(false);

async function handleTap() {
  if (completed || pending) return;
  setCompleted(true);  // optimistic
  setPending(true);
  try {
    await appendCompletion({ ...itemData });
  } catch {
    setCompleted(false);  // revert on failure
    // show toast/error
  } finally {
    setPending(false);
  }
}
```

### Pattern 4: Session State via React Context (no persistence)

**What:** Location, shift, and staff name stored in React Context (in-memory only). Refreshing the page returns to session-start screen.

**When to use:** All session-scoped data.

**Why NOT localStorage:** localStorage persists across page refreshes, creating ghost sessions. A hard refresh is the cleanest way to start a new session — we want that behavior.

### Pattern 5: Viewport Meta for Tablet Lock

**What:** Prevent pinch-zoom and enforce a stable viewport on the shared tablet.

```typescript
// src/app/layout.tsx
export const metadata = {
  viewport: {
    width: 'device-width',
    initialScale: 1,
    minimumScale: 1,
    maximumScale: 1,
    userScalable: false,
  },
};
```

### Pattern 6: Manager Dashboard Read (QUERY pre-computed in Sheet)

**What:** The Manager-View tab in the Sheet contains QUERY formulas that aggregate today's completions by location and shift. The Next.js dashboard route reads this tab and renders the pre-aggregated data — no aggregation happens in JS.

```typescript
// src/app/api/dashboard/route.ts
// Reads Manager-View tab, returns structured summary
const res = await sheets.spreadsheets.values.get({
  spreadsheetId: sheetId,
  range: "'Manager-View'!A1:Z50",
});
```

**Manager-View QUERY formula example (in the Sheet):**
```
=QUERY('Completions-Log'!A:H,
  "SELECT B, C, COUNT(E)
   WHERE A >= date '"&TEXT(TODAY(),"yyyy-mm-dd")&"'
   GROUP BY B, C
   LABEL COUNT(E) 'Items Completed'",
  1)
```

### Anti-Patterns to Avoid

- **Row-update writes:** Never use `spreadsheets.values.update` to edit an existing Completions-Log row. Always append new rows. Updates require knowing row numbers and can collide under concurrent access.
- **Client-side credentials:** The GOOGLE_SERVICE_ACCOUNT_KEY env var must be accessed only in Server Actions or API Route handlers — never in client components or `NEXT_PUBLIC_` vars.
- **localStorage for session state:** Causes ghost sessions on shared tablets. Use in-memory React state only.
- **Fixed column indices in Completions-Log reads:** Use named ranges or header-relative addressing when reading the Sheet — column order may shift.
- **shadcn/ui:** Not compatible with Tailwind v4 as of early 2026. Do not add it.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Google API auth | Custom JWT signing | `google.auth.GoogleAuth` from googleapis | Handles token refresh, expiry, retry — many edge cases |
| Exponential backoff | Custom retry loop | Pattern above (trivial to copy) | Sheets API enforces 300 writes/min per project; 429s will happen |
| Optimistic UI | Custom loading state logic | useState pattern above | Simple enough to not need a library (no React Query needed for this scale) |
| Checklist config | Build a CMS | Hardcoded `checklist-config.ts` for v1 | YAGNI — Rez isn't editing checklist items daily; add Sheet-driven config in v2 only if requested |
| Tablet kiosk mode | Custom PWA install flow | Bookmarked URL in Safari full-screen is sufficient | iPad/Android tablets support fullscreen bookmarks natively; no service worker complexity needed for v1 |

**Key insight:** The complexity in this phase is UX clarity (making the session-start screen impossible to misuse), not technical architecture. The Sheets write pattern is already solved in LeaseJenny.

---

## Common Pitfalls

### Pitfall 1: Ghost Sessions (Prior Shift Lingering on Tablet)
**What goes wrong:** Staff opens the tablet mid-shift and sees the previous crew's partially completed checklist. They continue checking items under the wrong shift/name.
**Why it happens:** Shared tablet, no user accounts, state persists if the browser tab stays open.
**How to avoid:** Use React state only (no localStorage/sessionStorage). Any page refresh resets to session-start. Make the session-start screen (location + shift + name) prominent and always the first thing rendered. The checklist UI should show the active session info (location, shift, name) persistently in a header — staff can immediately see if it's a ghost session.
**Warning signs:** Staff names on Completions-Log that don't match the shift time.

### Pitfall 2: Concurrent Write Collision
**What goes wrong:** Two staff tap simultaneously; one row gets overwritten.
**Why it happens:** `spreadsheets.values.append` is not atomic across concurrent callers — two simultaneous calls find the same "next empty row" and one overwrites the other.
**How to avoid:** Single tablet per location means true simultaneous taps are rare. Use `INSERT_ROWS` as `insertDataOption` (not `OVERWRITE`) — this inserts a new row rather than writing to a detected empty row. Add exponential backoff on 429 responses. If Rez ever moves to multiple tablets per location, re-evaluate with Vercel KV as a write buffer.
**Warning signs:** Missing completion rows despite staff reporting they tapped items.

### Pitfall 3: Wrong Sheets Scope (Read-Only vs Read-Write)
**What goes wrong:** App deploys but write attempts return 403 PERMISSION_DENIED.
**Why it happens:** LeaseJenny uses `spreadsheets.readonly` scope — easy to copy that file and forget to change the scope.
**How to avoid:** Explicitly use `https://www.googleapis.com/auth/spreadsheets` (read-write) in `getAuth()`. Verify the service account has Editor access on the Checklist Sheet (not just Viewer).
**Warning signs:** `403 PERMISSION_DENIED` in Vercel function logs on any append call.

### Pitfall 4: Vercel Serverless Cold Start Latency on First Tap
**What goes wrong:** First checklist tap after inactivity takes 2-4 seconds; staff think the app is broken.
**Why it happens:** Vercel serverless functions cold-start on first invocation after idle period.
**How to avoid:** Optimistic UI (Pattern 3 above) means the item appears checked immediately — the write happens in background. Staff feel no latency because the UI responds instantly. Error-only feedback keeps the happy path invisible.
**Warning signs:** None in production — optimistic UI masks it.

### Pitfall 5: GOOGLE_SERVICE_ACCOUNT_KEY Encoding
**What goes wrong:** Service account JSON fails to parse at runtime.
**Why it happens:** The JSON key file must be base64-encoded before pasting into Vercel's env var field. Copy-pasting the raw JSON often introduces newlines or truncation.
**How to avoid:** Encode locally: `base64 -i service-account-key.json | tr -d '\n'` then paste the single-line result into Vercel. The decode in `getAuth()` reverses this exactly.
**Warning signs:** `SyntaxError: Unexpected token` in Vercel function logs.

### Pitfall 6: Manager Dashboard Shows No Data Before Today's First Write
**What goes wrong:** Dashboard shows empty/error before any shift has been completed today.
**Why it happens:** QUERY over Completions-Log with `WHERE date = TODAY()` returns zero rows; spreadsheet renders it as empty or `#N/A`.
**How to avoid:** Handle empty response in the API route gracefully — return `{ locations: [], date: today }` rather than throwing. Dashboard UI should render "No activity yet today" states rather than error messages.
**Warning signs:** Dashboard shows blank or error at 6am before opening shifts start.

---

## Code Examples

### Completions-Log Append (Verified Pattern)

```typescript
// Source: Google Sheets API docs + LeaseJenny lib/sheets.ts pattern
await sheets.spreadsheets.values.append({
  spreadsheetId: sheetId,
  range: "'Completions-Log'!A:H",
  valueInputOption: 'USER_ENTERED',     // allows date parsing in Sheet
  insertDataOption: 'INSERT_ROWS',      // insert new row — do NOT use OVERWRITE
  requestBody: {
    values: [[
      new Date().toISOString(),          // A: Timestamp
      location,                          // B: Location
      shift,                             // C: Shift (Opening/Closing)
      staffName,                         // D: StaffName
      itemId,                            // E: ItemID
      itemText,                          // F: ItemText
      category,                          // G: Category
      notes,                             // H: Notes (empty string if none)
    ]],
  },
});
```

### Read-Write Auth Scope (differs from LeaseJenny)

```typescript
// LeaseJenny uses .readonly — checklist app MUST use read-write
const auth = new google.auth.GoogleAuth({
  credentials: keyJson,
  scopes: ['https://www.googleapis.com/auth/spreadsheets'],  // read + write
});
```

### Viewport Meta for Tablet Lock

```typescript
// src/app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Shift Checklist',
  // Next.js 16 supports viewport as part of metadata
};

export const viewport = {
  width: 'device-width',
  initialScale: 1,
  minimumScale: 1,
  maximumScale: 1,
  userScalable: false,
};
```

### Checklist Config Structure (hardcoded v1)

```typescript
// src/lib/checklist-config.ts
export type ShiftType = 'Opening' | 'Closing';
export type Category = 'Opening Procedures' | 'Closing Procedures' | 'Cleaning & Sanitation' | 'Equipment Checks';

export interface ChecklistItem {
  id: string;
  category: Category;
  shift: ShiftType | 'Both';  // 'Both' = appears on all shifts
  text: string;
  locationOverride?: string[];  // if set, only show for listed locations
}

// Items are filtered at render time: show if shift matches + no locationOverride OR location in locationOverride
export const CHECKLIST_ITEMS: ChecklistItem[] = [
  { id: 'open-001', category: 'Opening Procedures', shift: 'Opening', text: 'Check in with manager on duty' },
  { id: 'clean-001', category: 'Cleaning & Sanitation', shift: 'Both', text: 'Sanitize prep surfaces' },
  // ... etc
];

export const LOCATIONS = [
  'Moto Medi Lubbock 1',
  'Moto Medi Lubbock 2',
  'Moto Medi Amarillo',
  'Tikka Shack 1',
  'Tikka Shack 2',
] as const;

export type Location = typeof LOCATIONS[number];
```

### Manager-View QUERY (in the Sheet, not in code)

```
=QUERY('Completions-Log'!A:H,
  "SELECT B, C, D, COUNT(E) WHERE DATEDIF(A, now(), 'D') = 0 GROUP BY B, C, D LABEL COUNT(E) 'count'",
  1)
```

Note: DATE filtering in QUERY uses DATEDIF or date literal. Test this formula against actual Completions-Log data before finalizing — QUERY date handling against ISO strings may need a helper column.

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `next-pwa` for offline | Serwist or manual service worker | 2024-2025 | `next-pwa` conflicts with Turbopack; Serwist is the new recommendation |
| Tailwind v3 | Tailwind v4 | 2025 | v3 `fs` resolution bug with Turbopack makes v4 required for Next.js 15+ |
| `pages/` API routes for Server Actions | `app/` Server Actions (`'use server'`) | Next.js 13+ | Server Actions run entirely server-side; no API route boilerplate needed for writes |
| shadcn/ui | Not yet — Tailwind v4 incompatibility | Early 2026 | shadcn/ui does not fully support Tailwind v4 yet; avoid |

**Deprecated/outdated:**
- `next-pwa` (original): webpack-only, conflicts with Turbopack — do not use
- `react-papaparse`: unmaintained — not needed for this phase anyway
- Tailwind v3 `@apply` patterns: v4 uses different config syntax

**PWA for v1:** Do NOT build a service worker or full PWA for v1. A bookmarked URL in Safari/Chrome on the tablet is sufficient. Serwist is available if v2 requires offline support, but adds config complexity that is not justified for this phase.

---

## Open Questions

1. **Checklist items for each location and shift**
   - What we know: Four categories (opening, closing, cleaning, equipment). Shift types: Opening and Closing.
   - What's unclear: The actual line items. This cannot be invented — it must come from Rez or existing SOPs.
   - Recommendation: Before building, get Rez to provide a list of checklist items per shift. Even a rough list is fine — hardcode in `checklist-config.ts` for v1. If unavailable at build time, stub with 3-4 placeholder items per category so the app is functional for review.

2. **Manager-View QUERY date filtering reliability**
   - What we know: Sheets QUERY can filter by date. ISO timestamps in column A need date conversion.
   - What's unclear: Whether `QUERY` handles ISO 8601 strings from `toISOString()` natively, or whether a helper column is needed (e.g., `=DATEVALUE(LEFT(A2,10))`).
   - Recommendation: Create the Sheet manually during Wave 0, test the QUERY formula against a few sample rows before wiring up the dashboard API route. If QUERY can't filter ISO strings reliably, use a helper column in the Sheet.

3. **Concurrent tablet usage volume**
   - What we know: The project blocker noted in STATE.md: "Confirm expected concurrent tablet usage volume before committing to direct Sheets writes vs. Vercel KV write buffer."
   - What's unclear: Whether any location has multiple tablets or staff that would simultaneously tap items.
   - Recommendation: Proceed with direct Sheets append for v1 (one tablet per location). If Rez mentions multiple devices at a single location, add Vercel KV as a write buffer in that wave. Do not over-engineer upfront.

---

## Validation Architecture

nyquist_validation is enabled (config.json: `"nyquist_validation": true`).

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Jest + React Testing Library (to be installed — not yet in project) |
| Config file | `jest.config.ts` — Wave 0 gap |
| Quick run command | `npx jest --testPathPattern=checklist-config --passWithNoTests` |
| Full suite command | `npx jest --passWithNoTests` |

Note: This is a new standalone project with no existing test infrastructure. All framework setup is a Wave 0 task.

### Phase Requirements to Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CHK-01 | Location + shift selector renders all 5 locations and 2 shifts | unit | `npx jest src/__tests__/LocationShiftSelector.test.tsx` | Wave 0 |
| CHK-02 | Name entry renders and passes name to session context | unit | `npx jest src/__tests__/NameEntry.test.tsx` | Wave 0 |
| CHK-03 | Checklist config returns correct items for each location/shift combo | unit | `npx jest src/__tests__/checklist-config.test.ts` | Wave 0 |
| CHK-04 | Tapping item calls appendCompletion with correct params | unit (mock Server Action) | `npx jest src/__tests__/ChecklistItem.test.tsx` | Wave 0 |
| CHK-05 | Notes field renders on item expand; value included in appendCompletion call | unit | `npx jest src/__tests__/ChecklistItem.notes.test.tsx` | Wave 0 |
| CHK-06 | appendCompletion builds correct row array and calls sheets.append | unit (mock googleapis) | `npx jest src/__tests__/actions.completions.test.ts` | Wave 0 |
| CHK-07 | Dashboard API route returns location/shift summary from Manager-View tab | unit (mock sheets response) | `npx jest src/__tests__/api.dashboard.test.ts` | Wave 0 |
| CHK-08 | `next build` exits 0 | smoke | `npx next build` | N/A — run manually |
| CHK-09 | Viewport meta includes `maximum-scale=1` / `user-scalable=no` | unit | `npx jest src/__tests__/layout.test.tsx` | Wave 0 |

### Sampling Rate
- **Per task commit:** `npx jest --passWithNoTests`
- **Per wave merge:** `npx jest --passWithNoTests` + manual tablet test (verify tap targets, no zoom)
- **Phase gate:** Full suite green + manual tablet review before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `src/__tests__/LocationShiftSelector.test.tsx` — covers CHK-01
- [ ] `src/__tests__/NameEntry.test.tsx` — covers CHK-02
- [ ] `src/__tests__/checklist-config.test.ts` — covers CHK-03
- [ ] `src/__tests__/ChecklistItem.test.tsx` — covers CHK-04
- [ ] `src/__tests__/ChecklistItem.notes.test.tsx` — covers CHK-05
- [ ] `src/__tests__/actions.completions.test.ts` — covers CHK-06
- [ ] `src/__tests__/api.dashboard.test.ts` — covers CHK-07
- [ ] `src/__tests__/layout.test.tsx` — covers CHK-09
- [ ] `jest.config.ts` — Jest + React Testing Library config
- [ ] `jest.setup.ts` — RTL setup file
- [ ] Framework install: `npm install --save-dev jest @testing-library/react @testing-library/jest-dom jest-environment-jsdom @types/jest ts-jest`

---

## Sources

### Primary (HIGH confidence)
- LeaseJenny dashboard source at `/Users/josi/leasejenny-dashboard/src/lib/sheets.ts` — exact auth pattern to replicate
- LeaseJenny `package.json` — exact versions: Next 16.1.6, React 19.2.3, googleapis ^171.4.0, Tailwind ^4
- [Google Sheets API Usage Limits](https://developers.google.com/workspace/sheets/api/limits) — 300 writes/min per project, 60/min per user; 429 is expected and must be handled
- [Next.js PWA Guide](https://nextjs.org/docs/app/guides/progressive-web-apps) — official recommendation for service workers; Serwist for offline support
- [spreadsheets.values.append docs](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/append) — INSERT_ROWS vs OVERWRITE behavior
- Project SUMMARY.md — architecture decisions, pitfall list, confirmed stack

### Secondary (MEDIUM confidence)
- [Concurrent Sheets append collision evidence](https://groups.google.com/g/google-spreadsheets-api/c/G0sUsBHlaZg) — community report; INSERT_ROWS is safer than OVERWRITE for concurrent callers
- [Next.js offline PWA discussion](https://github.com/vercel/next.js/discussions/82498) — confirms Serwist approach for offline; not needed for v1

### Tertiary (LOW confidence)
- QUERY date filtering against ISO strings — untested assumption; must be validated in Wave 0 against real Sheet data

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — exact versions copied from LeaseJenny which is working in production
- Architecture: HIGH — append-only Sheets pattern is documented and proven; session state via React context is standard
- Pitfalls: HIGH — ghost session, scope mismatch, and Sheets concurrent write issues are all verified against official docs and existing project source
- Checklist item content: LOW — actual line items must come from Rez; cannot be researched

**Research date:** 2026-03-14
**Valid until:** 2026-06-14 (90 days — stable stack, no fast-moving dependencies)
