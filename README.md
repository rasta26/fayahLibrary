# fayahLibrary

Gerry's personal Claude Code library. Clone, type `install`, done.

```bash
git clone https://github.com/<you>/fayahLibrary.git
cd fayahLibrary
./install            # or: make install
```

`./install` registers this repo as a Claude Code plugin marketplace, installs the
`fayah-core` plugin at user scope, and adds the default MCP servers. Restart Claude Code
afterwards.

## What you get

| Kind | Items |
|------|-------|
| **Skills** | `code-quality-review`, `event-tracking`, `spec-first-tdd`, `manager-orchestration`, `mentoring-code-review`, `coding-kata` |
| **Agents** | `manager`, `spec-writer`, `test-writer`, `backend-implementer`, `frontend-implementer`, `integrator` |
| **Commands** | `/cleanup-audit`, `/add-tracking`, `/spec`, `/orchestrate`, `/review`, `/kata` |
| **Hook** | `PostToolUse` → local tool-usage log at `~/.fayah/events.jsonl` (feature-usage telemetry for your own sessions; nothing leaves the machine) |
| **MCP (default)** | `sequential-thinking`, `memory`, `context7`, `mcp-compass` |
| **MCP (optional)** | `github`, `playwright`, `postgres`, `mcp-installer` → `./install --mcp <name>` |
| **External (optional)** | Task Master, SuperClaude, Claude Swarm, Claude Code Router, MCPHub, aider, OpenHands, the awesome-lists and Anthropic cookbooks → `./install --external` |

How the skills fit together: `/spec` writes requirements and contracts → `/orchestrate`
runs the manager, which dispatches sub-agents that each TDD one requirement and merge into the
shared branch → `/review` for mentoring review of the result → `/cleanup-audit` and
`/add-tracking` for existing codebases → `/kata` to turn review findings into practice.

## Security gate: SkillSpector

Every skill, agent, command and MCP config in this repo is scanned with
[NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector) before it is committed.

```bash
make check     # offline structural + static checks (no deps)
make scan      # installs skillspector if missing, scans, non-zero exit on findings
make hooks     # git pre-commit hook that runs both
```

CI (`.github/workflows/scan.yml`) repeats the scan on every PR and uploads the JSON report.
Third-party tools installed via `./install --external` are scanned on clone when they contain
skills or MCP config.

## Layout

```
.claude-plugin/marketplace.json   this repo as a marketplace
plugins/fayah-core/               the plugin: skills/ agents/ commands/ hooks/ .mcp.json
mcp/servers.json                  curated MCP servers (default + optional)
external/catalog.json             vetted third-party tools, plus what was dropped and why
scripts/check.py                  offline checks; scripts/pre-commit
docs/CATALOG.md                   how the source list was triaged
install, Makefile
```

## Adding a skill

1. `mkdir plugins/fayah-core/skills/<name>` and write `SKILL.md` with `name` (== dir) and a
   `description` that says *when* to use it.
2. `make check && make scan`.
3. Commit; `claude plugin marketplace update fayah-library && claude plugin install fayah-core@fayah-library`.

## Uninstall

`./install --uninstall`
