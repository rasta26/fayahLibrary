# Template: Codebase cleanup audit

## 1. Purpose
A maintainability audit of a codebase: dead code, duplicates, unused UI, needless complexity, legacy code,
redundant queries, abandoned files and tech debt, plus a cleanup plan. A report only; nothing is deleted.
For me and the team that owns the code. Full method: `code-quality-review` skill.

## 2. Inputs
- Repo path or URL, and the commit to audit (required; default: latest on main)
- Scope (default: whole repo)
- Off-limits areas, e.g. public APIs (ask if the repo serves other teams)
- Whether tests and tooling can be run here (if not, say which evidence is missing)

## 3. Steps
1. Map entry points, build config and dependencies.
2. Run the tests to get a baseline.
3. For each of the 8 categories, gather evidence with commands and search, not guesses.
4. Write each finding in the fixed block. Anything without evidence goes under Needs confirmation.
5. Group findings into PR-sized steps, lowest risk first. Every step gets a real pre-check
   (never "none") and a rollback. If tests are missing, adding them is step 1.
6. List what not to touch yet. Confirm the repo was left unchanged.

## 4. Output format
```
# Cleanup audit: <repo> (<date>)
Commit: <sha> · Scope: <scope> · Tests: <command → result>
## Summary
| # | Category | Findings | High confidence |   (all 8 rows; "none found" or "n/a: why")
## Findings
### [CATEGORY] <short title>
- Location: <path:line>
- Why unnecessary: <evidence: the command or search that proved it, and its result>
  (for TECH DEBT, label this line "Problem:" instead)
- Impact of removal: <lines removed, risk reduced, who benefits>
- Risk before deletion: <what could break>
- Confidence: high | medium | low
## Needs confirmation
## Cleanup plan
| Step | Change | Pre-checks | Rollback |
## Don't touch yet
```
Tone: plain and factual; findings, not opinions.

## 5. Finished example
`delivery/examples/2026-11-16-azure-logs-mcp-audit.md`

## 6. Done check
- [ ] Every finding has a file location and a command or search with its result; reading a file alone isn't proof.
- [ ] All 8 categories appear in the summary, each with a finding count, "none found" or "n/a" plus a reason.
- [ ] The plan runs lowest risk first, and every step has a pre-check and a rollback.
- [ ] Claims without evidence are under Needs confirmation, not Findings.
- [ ] The audited repo is unchanged (git status clean).
