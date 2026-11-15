# Source list triage

The library started from a shared list of 20 Claude / MCP / coding-agent repos. Selection
criteria: does it serve principal-engineer work (code review, mentoring, coding practice,
picking up languages, learning AI development) and the spec-first / TDD / manager-sub-agent
workflow? Everything else was dropped or linked only.

| Source item | Decision | Where |
|-------------|----------|-------|
| anthropics/claude-code | host platform | prerequisite |
| anthropics/claude-cookbooks | keep, reference | `external` → `claude-cookbooks` |
| anthropics/claude-quickstarts | keep, reference (kata bases) | `external` → `claude-quickstarts` |
| Claude Desktop Extensions (dxt → mcpb) | drop | only for shipping Desktop extensions |
| hesreallyhim/awesome-claude-code | keep, skill source | `external` → `awesome-claude-code` |
| punkpeye/awesome-mcp-servers | keep, MCP source | `external` → `awesome-mcp-servers` |
| SuperClaude-Org/SuperClaude_Framework | keep, optional plugin | `external` → `superclaude` |
| musistudio/claude-code-router | keep, optional | `external` → `claude-code-router` |
| eyaltoledano/claude-task-master | keep, optional (spec → tasks) | `external` → `claude-task-master` |
| Doriandarko/claude-engineer | drop | superseded by Claude Code |
| Claude Swarm (listed as parallaxsys) | keep, corrected to parruda/swarm | `external` → `claude-swarm` |
| Claude Dev Tools (zebbern) | drop | repo not found; zebbern/claude-code-guide is docs |
| liuyoshio/mcp-compass | keep, default MCP | `mcp/servers.json` |
| anaisbetts/mcp-installer | keep, optional MCP | `mcp/servers.json` |
| MCPHub (listed as idosal) | keep, corrected to samanhappy/mcphub, optional | `external` → `mcphub` |
| continuedev/continue | drop | IDE extension outside this workflow |
| cline/cline | drop | IDE extension outside this workflow |
| OpenInterpreter/open-interpreter | drop | not a coding-review tool |
| Aider-AI/aider | keep, optional | `external` → `aider` |
| OpenDevin → OpenHands/OpenHands | keep, optional reference | `external` → `openhands` |

Added beyond the list: `sequential-thinking`, `memory`, `context7`, `github`, `playwright`,
`postgres` MCP servers, and NVIDIA SkillSpector as the mandatory scan gate.

## Why the skills are custom rather than imported

The user's stated workflow (specs first, design by contract, isolated front end/back end,
manager + small sub-agents, continuous integration into one branch, TDD per requirement, a
fixed audit format, a fixed set of nine telemetry families) is specific enough that imported
general-purpose skills would need rewriting anyway. The six skills encode that workflow
directly; the awesome-lists are kept as sources for future additions, each to be scanned
before import.
