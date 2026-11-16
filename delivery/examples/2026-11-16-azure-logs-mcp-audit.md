# Cleanup audit: rasta26/azure-logs-mcp (2026-11-16)
Commit: 0131910 · Scope: whole repo · Tests: none exist (CLAUDE.md:20). Azure packages could not be
installed in the audit environment, so the server was not started; all files compile (`python3 -m py_compile`).

## Summary
| # | Category | Findings | High confidence |
|---|----------|----------|-----------------|
| 1 | Dead code | 5 | 4 |
| 2 | Duplicate logic | 3 | 3 |
| 3 | Unused UI components | n/a: no UI | – |
| 4 | Over-complex implementations | none found (450-line single dispatch is proportionate for 15 tools) | – |
| 5 | Legacy code | 1 | 1 |
| 6 | Redundant queries / API calls | 1 | 0 |
| 7 | Abandoned files | 1 | 1 |
| 8 | Technical debt | 4 | 3 |

## Findings
### [DEAD CODE] alerts.py is never imported
- Location: alerts.py:5 (`AlertManager`, 87 lines); Dockerfile:8 copies it
- Why unnecessary: `grep -rn "AlertManager\|import alerts" --include=*.py .` matches only the definition; CLAUDE.md:7 says it "isn't exposed as tools"
- Impact of removal: −87 lines, drops `azure-mgmt-monitor` from requirements.txt:4, smaller image
- Risk before deletion: it was deliberately repaired on Oct 4 (tasks/todo.md item 10), so it may be planned work
- Confidence: medium

### [DEAD CODE] Unused dependency azure-mgmt-resource
- Location: requirements.txt:5
- Why unnecessary: `grep -rn "mgmt.resource" --include=*.py .` returns nothing; tasks/todo.md review also flags it
- Impact of removal: faster install, smaller image
- Risk before deletion: none known; check a clean-venv install still starts
- Confidence: high

### [DEAD CODE] get_security_query() never called
- Location: security_queries.py:44–46
- Why unnecessary: `grep -rn "get_security_query\b"` hits only the definition and tool-name strings; server.py:401 reads `SECURITY_QUERIES` directly
- Impact of removal: −3 lines; one way to read templates
- Risk before deletion: none (not imported anywhere)
- Confidence: high

### [DEAD CODE] Unused variable kql_keywords
- Location: server.py:95
- Why unnecessary: an AST scan of assigned-but-never-read names finds only `kql_keywords`
- Impact of removal: −1 line; removes the impression that keywords are checked
- Risk before deletion: none
- Confidence: high

### [DEAD CODE] Unreachable empty-result branches
- Location: server.py:67–68 and 75–76
- Why unnecessary: `grep -n "if not results:\|if not limited_results:" server.py` → 61, 67, 75: line 61 already returns on empty input, so 67 and 75 can never fire
- Impact of removal: −4 lines
- Risk before deletion: none
- Confidence: high

### [DUPLICATE] mcp.json and mcp-config.json are identical
- Location: mcp.json, mcp-config.json (and the same server in .vscode/settings.json:3)
- Why unnecessary: `diff mcp.json mcp-config.json` prints nothing; README.md:78 documents only mcp-config.json
- Impact of removal: one config to maintain; both hard-code `/Users/fayah/...`, unusable by anyone else
- Risk before deletion: confirm no client of yours reads `mcp.json` by that name
- Confidence: high

### [DUPLICATE] query_security_logs repeats query_logs
- Location: server.py:413–415 vs 313–315
- Why unnecessary: `grep -n 'run_query(get_workspace(arguments), arguments\["query"\]' server.py` → 314 and 414 are the same call; only the default timespan differs (PT1H vs PT24H) and 414 lacks `limit`
- Impact of removal: one fewer tool for the model to choose between
- Risk before deletion: tool names are a public contract; prompts may call it. Keep as a thin alias first
- Confidence: high

### [DUPLICATE] CSV writing in two places
- Location: server.py:69–73 and 386–389
- Why unnecessary: `grep -n "csv.DictWriter" server.py` → 70 and 387: the same write sequence, once to a string and once to a file
- Impact of removal: one helper; ~4 lines
- Risk before deletion: low
- Confidence: high

### [LEGACY] tasks/todo.md is a finished work log
- Location: tasks/todo.md (103 lines)
- Why unnecessary: `grep -c "\- \[ \]"` = 0 open, 15 done; Part 1 describes the removed Node server
- Impact of removal: −103 lines of stale guidance an agent may follow
- Risk before deletion: its "Not verified / follow-ups" list is the only record of open work; move to issues first
- Confidence: high

### [REDUNDANT QUERY] list_tables scans 30 days of data to get table names
- Location: server.py:368 (`search * | distinct $table`, P30D)
- Why unnecessary: `grep -n "search \*" server.py` → line 368 runs `search * | distinct $table` over P30D, which reads every row to produce a name list; the already-installed `azure-mgmt-loganalytics` can list tables as metadata
- Impact of removal: large cost and latency drop on busy workspaces
- Risk before deletion: the metadata API needs subscription and resource group, and also lists empty tables; changes output
- Confidence: medium (no real workspace to measure)

### [ABANDONED] .DS_Store committed despite .gitignore
- Location: .DS_Store
- Why unnecessary: `git ls-files | grep -i ds_store` returns it; .gitignore:4 ignores it
- Impact of removal: clean tree
- Risk before deletion: none
- Confidence: high

### [TECH DEBT] No tests
- Location: repo root (CLAUDE.md:20 "There are no tests or linter")
- Problem: `find . -name "test_*.py" -o -name "*_test.py" -o -name tests` finds 0; the Oct 4 mocked-client checks were run by hand and not saved
- Impact of fixing: every cleanup step below can be verified; blocks regressions like the mcp 2.x crash
- Risk: none
- Confidence: high

### [TECH DEBT] export_results writes anywhere and ignores timespan
- Location: server.py:380–394
- Problem: `grep -n 'filename = arguments\|open(filename\|"PT24H")$' server.py` → lines 380, 386, 391: caller's `filename` goes straight to `open()`; line 381 hard-codes PT24H; in Docker `/app` isn't writable by `nobody` (tasks/todo.md follow-ups)
- Impact of fixing: no arbitrary file writes; tool works in the container
- Risk: callers relying on absolute paths
- Confidence: high

### [TECH DEBT] validate_query accepts almost anything
- Location: server.py:89–101
- Problem: running the function: `"this is not kql at all"` → `(True, 'Valid syntax')`
- Impact of fixing: the tool stops giving false confidence
- Risk: low; options are to rename it or validate with a `| take 0` query
- Confidence: high

### [TECH DEBT] docker-compose doesn't pass DEFAULT_WORKSPACE_ID or DEBUG
- Location: docker-compose.yml:6–10 vs .env.example:7,13
- Problem: `grep -n "DEFAULT_WORKSPACE_ID\|DEBUG" docker-compose.yml` finds nothing, so the container ignores two documented settings
- Impact of fixing: container behaves like a local run
- Risk: none
- Confidence: medium (Docker not run)

## Needs confirmation
- Whether alerts.py is planned work (decides finding 1).
- Saved queries live only in memory (server.py:29) and vanish on restart: intended?
- `version: '3.8'` in docker-compose.yml is obsolete in Compose v2; not checked because Docker couldn't run.

## Cleanup plan
| Step | Change | Pre-checks | Rollback |
|------|--------|------------|----------|
| 1 | Add tests: format_results, validate_kql_syntax, get_workspace, dispatch with a mocked client | new tests pass against unchanged code (they describe today's behaviour) | revert PR |
| 2 | Zero-risk deletions: kql_keywords, unreachable branches, get_security_query, untrack .DS_Store | tests green; tools/list shows 15 tools | revert PR |
| 3 | Drop azure-mgmt-resource | clean-venv install; server starts | revert PR |
| 4 | Remove mcp.json; make mcp-config.json path-neutral | confirm nothing reads mcp.json | revert PR |
| 5 | Move todo.md follow-ups to issues, then archive tasks/todo.md | issues created | revert PR |
| 6 | Fix export_results (output folder + timespan), compose env vars, validate_query | tests for each | revert PR |
| 7 | query_security_logs → alias of query_logs; list_tables via metadata API | check prompts/clients using these tools; test on a real workspace | revert PR |
| 8 | Decide alerts.py: expose as tools or archive | your decision | revert PR |

## Don't touch yet
- Tool names and input schemas until step 7's usage check; they're the server's public contract.
- alerts.py until you decide on it.
