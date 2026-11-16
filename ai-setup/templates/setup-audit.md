# Template: AI setup audit

## 1. Purpose
Find everything my AI setup loads, score what earns its place, and propose a job-based folder structure
with a map. Nothing is moved until I approve. For me.

## 2. Inputs
- Nothing required: default scope is everything reachable (claude.ai instructions, memory, Projects,
  skills, plugins, connectors, scheduled tasks, artifacts, GitHub repos, Drive, local instruction files)
- Ask: anything to leave out, and any history source I can point to

## 3. Steps
1. Inventory each source with tools. Record name, location, what it claims, size, last changed or used.
   Write "unknown" when a date can't be found; never estimate.
2. Score each item KEEP / MERGE / CUT / UNSURE with a one-line reason. Strict: if a good model
   would do it without the instruction, CUT. Every MERGE names its partner.
3. Propose one folder per job, with shared preferences in one place at the top.
4. Draft a map of 60 lines or fewer that points to things and never repeats them.
5. List the exact moves in order, marking the ones I must do myself. Stop for approval.
6. After approval: work on a branch, move repo items to `_archive/<date>/`, put personal
   items in a private Drive folder (never a public repo), open a PR, and verify nothing was lost.

## 4. Output format
1. What I could and couldn't see (2–3 lines)
2. The biggest finding (2–3 lines)
3. Item table grouped by source: # · item (what it does) · size · last changed · score: reason
4. Counts: total, KEEP, MERGE, CUT, UNSURE, and the rough share the cuts remove
5. Proposed tree
6. Draft map
7. Ordered steps, with "You:" on the ones I do
Plain language, no jargon.

## 5. Finished example
`ai-setup/examples/2026-11-16-setup-audit.md`

## 6. Done check
- [ ] Every date is real or "unknown".
- [ ] Every MERGE names its partner.
- [ ] The counts add up to the total.
- [ ] The map is 60 lines or fewer and repeats no content.
- [ ] Nothing was changed before approval, and nothing personal is headed for a public repo.
