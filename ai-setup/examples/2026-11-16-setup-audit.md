# Example: AI setup audit (2026-11-16)

The real audit delivered on 2026-11-16, before approval. One personal line is redacted because this repo is public.

**What I could see:** Claude custom instructions, saved memory, the one doc made in Claude, 8 connectors,
14 built-in skills, GitHub repos (`fayahLibrary` and `prompts` read in full) and Google Drive.
Nothing found: custom GPTs (no access), CLAUDE.md or AGENTS.md files, scheduled tasks, Claude-account
plugins, AI working docs in Drive. Usage history of connectors and built-in skills is not visible, so
those are UNSURE rather than guessed.

**Biggest finding:** the custom instructions hold a whole code-cleanup and event-tracking job that loads
into every chat, and the same content already lives, in more detail, in four `fayahLibrary` skills.

## 1. Every item

**Instructions and prompts**
| # | Item | Size | Last changed | Score: reason |
|---|---|---|---|---|
| 1 | Claude custom instructions (code audit, 9 tracking types, specs-first, manager agents, TDD) | ~45 lines | unknown | MERGE: already in skills 11–14; shrink to a 5-line preferences file |
| 2 | `prompts/ultrathink.MD` (pep talk persona) | 26 lines | Jan 2 | CUT: nothing loads it; useful parts already in skill 13 |
| 3 | `prompts/README.md` | 1 line | Dec 15, 2025 | CUT: empty |

**Saved memory**
| # | Item | Size | Last changed | Score: reason |
|---|---|---|---|---|
| 4 | Profile (principal engineer) | 2 lines | Oct 21 | KEEP: shapes depth of answers |
| 5 | Weekly work (review 4h, 1:1s, practice exercises) | 6 lines | Oct 21 | KEEP: defines the jobs |
| 6 | Gmail inbox system | 2 lines | Nov 11 | KEEP: active project |
| 7 | Learning AI development | 2 lines | Sep 30 | MERGE into #5 |
| 8 | (personal notes file, redacted) | 2 lines | Oct 13 | UNSURE: personal |
| 9 | fayahLibrary note (SkillSpector rule) | 2 lines | Nov 15 | KEEP: a rule the model can't guess |

**Claude workspace**
| # | Item | Last changed | Score: reason |
|---|---|---|---|
| 10 | "Gmail Inbox System" doc | Nov 11 | KEEP: finished work |
| 77 | One Claude Project (contents not visible) | unknown | UNSURE |

**fayahLibrary** (created Nov 15)
| # | Item | Score: reason |
|---|---|---|
| 11–16 | Skills: code-quality-review, event-tracking, spec-first-tdd, manager-orchestration, mentoring-code-review, coding-kata | KEEP: each encodes a fixed format or workflow |
| 17 | manager agent | MERGE: repeats skill 14 |
| 18–22 | spec-writer, test-writer, backend-implementer, frontend-implementer, integrator | KEEP: tool limits and file ownership |
| 23, 24, 27, 28 | /cleanup-audit, /add-tracking, /review, /kata | KEEP |
| 25, 26 | /spec, /orchestrate | MERGE: same as their agents |
| 29 | Usage-logging hook | CUT: log nothing reads |
| 30 | Plugin `.mcp.json` | MERGE: duplicates `mcp/servers.json` |
| 31, 32, 34, 38 | sequential-thinking, memory, mcp-compass, mcp-installer | CUT: default behaviour or duplicates |
| 33, 35 | context7, github | KEEP |
| 36, 37, 44 | playwright, postgres, Claude Code Router | UNSURE |
| 39 | Reference links | MERGE into one reading list |
| 40 | SkillSpector | KEEP: required scan |
| 41–43, 45–47 | SuperClaude, Task Master, Claude Swarm, MCPHub, aider, OpenHands | CUT: duplicate own skills or outside workflow |
| 48 | `docs/CATALOG.md` | CUT: history, repeated elsewhere |
| 49, 50 | README, plumbing | KEEP |

**Connectors and built-in skills**
| # | Item | Score: reason |
|---|---|---|
| 51 | Gmail | KEEP: used Nov 11 |
| 52–57 | Drive, Calendar, Figma, Spotify, Supabase, Composio | UNSURE: usage not visible |
| 58 | Hugging Face | CUT: setup never finished |
| 59 | docs | KEEP: used Nov 11 |
| 60–72 | other built-in skills | UNSURE: usage not visible |

**Other repos:** 73 azure-logs-mcp UNSURE · 74 azure_log_mcp MERGE into 73 · 75 mcp-graphapi UNSURE · 76 eleven older repos UNSURE.

## 2. Count
77 items: 27 KEEP, 8 MERGE, 15 CUT, 27 UNSURE. Cuts and merges remove about 20% of written
instructions by length (~240 of ~1,250 lines), and ~40 lines from what loads into every chat.

## 3–5
Tree, map and ordered steps: see `MAP.md` and pull request #1, which applied them after approval.
