# fayahLibrary

Gerry's personal Claude Code library, one plugin per job. Clone, type `install`, done.
Agents: start at [MAP.md](MAP.md).

```bash
git clone https://github.com/rasta26/fayahLibrary.git
cd fayahLibrary
./install            # or: make install
```

`./install` registers this repo as a Claude Code plugin marketplace, installs the three
plugins at user scope, and adds the default tools from `shared/mcp.json`. Restart Claude Code
afterwards. Add an optional tool with `./install --mcp <name>`.

| Plugin | Folder | Commands |
|--------|--------|----------|
| `fayah-review` | `code-review/` | `/review` |
| `fayah-coaching` | `coaching/` | `/kata` |
| `fayah-delivery` | `delivery/` | `/spec`, `/orchestrate`, `/add-tracking`, `/cleanup-audit` |

## Security gate: SkillSpector

Every skill, agent, command and tool setting is scanned with
[NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector) before it is committed.

```bash
make check     # offline structural + static checks (no deps)
make scan      # installs skillspector if missing, scans, non-zero exit on findings
make hooks     # git pre-commit hook that runs both
```

CI (`.github/workflows/scan.yml`) repeats the scan on every pull request.

## Adding a skill

1. `mkdir <job-folder>/skills/<name>` and write `SKILL.md` with `name` (== folder) and a
   `description` that says *when* to use it. New job? Copy a job folder's shape and add it to
   `.claude-plugin/marketplace.json` and `MAP.md`.
2. `make check && make scan`.
3. Commit, then `claude plugin marketplace update fayah-library` and reinstall the plugin.

## Uninstall

`./install --uninstall` (also removes the older single `fayah-core` plugin if present).
