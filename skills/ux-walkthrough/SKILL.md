---
name: ux-walkthrough
description: >-
  This skill should be used when the user asks to "run a UX walkthrough",
  "test the UX", "simulate a user", "persona walkthrough", "check the page
  from a user's perspective", "UX review with persona", or wants to evaluate
  a web page through the eyes of a simulated user persona. Browses live pages
  via Playwright, produces chain-of-thought inner voice, scores, and UX
  recommendations.
---

# UX Walkthrough

Simulate a real user persona browsing a live web page. Produce the persona's
inner voice as chain-of-thought, score each page, and list UX recommendations.

## Prerequisites

Playwright MCP must be available. If `browser_navigate` is not in the tool
list, abort with: "Playwright MCP is required for this skill."

## Phase 1 — Persona Creation

Collect persona parameters through interactive questions (AskUserQuestion).
Ask one question at a time in this order:

### 1.1 Age range

Options: 18-25 / 26-35 / 36-50 / 50+

### 1.2 Tech experience

| Level | Meaning |
|-------|---------|
| Tech-native | Builds or works with software daily |
| Moderate | Uses apps comfortably, doesn't build them |
| Tech-averse | Struggles with new interfaces, avoids technology |

### 1.3 Attention level

| Level | Behaviour |
|-------|-----------|
| High | Reads everything, inspects each element |
| Medium | Scans headings and prominent elements |
| Low | Glances for 3 seconds, clicks only the most obvious thing |

### 1.4 Platform familiarity

Options: First visit / Heard of it / Active user

### 1.5 Arrival context

How the persona arrives at the site — this determines starting dopamine:

| Scenario | Starting dopamine | Meaning |
|----------|-------------------|---------|
| Doomscrolling, came from Instagram/TikTok | High | Rapid-fire mode, needs instant reward to stay |
| Clicked a shared link | Medium-high | Curious but impatient, came for something specific |
| Google search result | Medium | Evaluating, comparing with other results |
| Friend recommended it | Medium | Willing to give it a chance, some trust |
| Bored, nothing to do | Low | Low energy, will browse passively, hard to engage |

### 1.6 Extra context (optional, free text)

Example: "Lives in a small town", "Has mild color blindness",
"Browsing on a phone in bright sunlight"

After collection, print a one-paragraph persona summary (including arrival
context and starting dopamine level) and ask for confirmation before
proceeding.

## Phase 2 — Live Browse

### Dopamine tracking

Dopamine is a **dynamic state** that changes throughout the session based on
what the persona experiences. It is NOT a fixed parameter — it shifts with
every page and interaction.

Start with the dopamine level determined by arrival context (Phase 1.5).
Track it as a value from 1-10 and update it after every page/interaction.

**What raises dopamine:**
- Visually appealing content (beautiful photos, clean design)
- Surprise or delight (unexpected content, clever interaction)
- Feeling of progress (clear next step, successful action)
- Social proof (activity indicators, other users' content)

**What lowers dopamine:**
- Confusion (unclear purpose, no obvious next action)
- Friction (forms, loading time, required sign-up)
- Boredom (walls of text, repetitive content, nothing new)
- Frustration (broken elements, errors, dead ends)

**How dopamine affects behaviour:**
- High (8-10): Actively exploring, clicking things, high tolerance for friction
- Medium (4-7): Browsing with moderate interest, will engage if something catches eye
- Low (1-3): Passive, about to leave, only a strong hook can save them
- Crashed (0): Leaves the site — walkthrough ends

Report the dopamine shift in each page's inner voice, e.g.:
> "Oh nice, beautiful photos! (dopamine: 5 → 7). I want to see more."
> "A registration form with 6 fields... (dopamine: 7 → 4). Ugh, maybe later."

### Navigation rules

Determine max page count from attention level:
- Low: 3-4 pages
- Medium: 5-6 pages
- High: 8-10 pages

These are upper limits — if dopamine crashes to 0, the persona leaves
regardless of remaining page budget.

For each page:

1. **Navigate** — `browser_navigate` to the URL.
2. **Capture** — Take a screenshot (`browser_take_screenshot`, type png)
   AND an accessibility snapshot (`browser_snapshot`).
3. **Inner voice** — Write the persona's stream-of-consciousness based on
   both the screenshot and the snapshot. The voice must reflect the persona's
   age, tech level, attention span, reading tolerance, AND current dopamine
   level. Include:
   - What the persona notices first
   - What confuses or frustrates them
   - Specific visual issues: color contrast, font size, button prominence,
     layout hierarchy, whitespace
   - Emotional reaction ("this looks trustworthy" / "feels like spam")
   - **Dopamine shift**: explicit before → after with reason
4. **Scores** — Rate the page on four criteria (1-10 each):
   - Understandability: Is the page's purpose clear?
   - Visual clarity: Is the layout clean, is hierarchy evident?
   - Accessibility: Contrast, touch targets, label quality
   - First impression: Gut feeling — would the persona stay?
   Include a short note explaining each score.
5. **Recommendations** — 2-5 actionable UX suggestions for this page.
6. **Next action** — Decide what the persona would do next. This decision
   is heavily influenced by current dopamine:
   - Click an element → use `browser_click` and continue the loop
   - Scroll → use `browser_press_key` (PageDown) and re-capture
   - Leave the site → break the loop and explain why (dopamine crashed)
   - Feel lost → report it and either go back or break

If credentials were provided at skill start, use them to log in when a
login page is encountered. Otherwise, stay on public pages only.

### Mental model calibration

| Parameter | Low | Medium | High |
|-----------|-----|--------|------|
| Tech experience | "What is this? Where do I click?" | "This must be the login" | "They're using lazy-loaded images, nice" |
| Attention span | First 3 seconds only | Scans the full viewport | Scrolls and inspects every section |
| Reading tolerance | Skips anything over 5 words | Reads headings + first sentence | Reads everything |
| Error tolerance | Leaves on first confusion | Tries once more | Investigates and retries |
| Dopamine (dynamic) | Passive, about to leave, needs strong hook | Browsing with interest, will engage if caught | Actively exploring, high friction tolerance |

## Phase 3 — Summary Report

After the browse loop ends, produce a final summary:

### Format

```
## UX Walkthrough Summary

**Persona:** [one-line summary]
**Pages visited:** N
**Estimated drop-off point:** [page name] — [reason]

### Dopamine Journey
[page 1]: ██████░░░░ 6 → "Nice photos, curious"
[page 2]: ████████░░ 8 → "This is fun, want more"
[page 3]: ████░░░░░░ 4 → "Registration wall, ugh"
[page 4]: ██░░░░░░░░ 2 → "Too many fields, leaving"

Peak: [page name] ([value]) — [why]
Lowest: [page name] ([value]) — [why]
Biggest drop: [page name] ([from] → [to]) — [why]

### Top 3 Critical Findings
1. ...
2. ...
3. ...

### Average Scores
| Criterion | Avg |
|-----------|-----|
| Understandability | X.X |
| Visual clarity | X.X |
| Accessibility | X.X |
| First impression | X.X |

### Priority Actions
1. ...
2. ...
3. ...
```
