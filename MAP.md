# Map: start here

Everything my AI setup uses lives here. Open only the folder you need.
This file only points; it never repeats what's inside.

## Shared preferences
- shared/preferences.md: how I like work done, for every job. Read first.
- The same text is in claude.ai custom instructions. Change both together.
- shared/mcp.json: the connected tools every job can use.

## Which folder for which request
| If the request is about...                                   | Open          |
|--------------------------------------------------------------|---------------|
| Reviewing a pull request or diff, PR feedback                 | code-review/  |
| A practice exercise or drill, for a mentee or for me          | coaching/     |
| Preparing a mentoring 1:1                                     | coaching/     |
| Auditing or reorganizing my AI setup                          | ai-setup/     |
| Building a feature: spec, contracts, tests, splitting work    | delivery/     |
| Adding analytics, monitoring or alerts to an app              | delivery/     |
| Cleaning up a codebase: dead code, duplicates, tech debt      | delivery/     |
| Learning a new language or AI development                     | learning/     |
| My email inbox system                                         | claude.ai doc "Gmail Inbox System" |
| Installing or adding to this library                          | README.md     |

## Inside each job folder
- skills/: the instructions for the job
- commands/: slash commands that start it
- agents/: helpers it hands work to (delivery/ only)
- templates/: blank starting points
- examples/: finished work worth copying

## Templates (use one whenever its job comes up)
- code-review/templates/pr-review.md: PR review
- coaching/templates/kata.md: practice exercise
- coaching/templates/one-on-one-prep.md: mentoring 1:1 prep
- delivery/templates/cleanup-audit.md: codebase cleanup audit
- ai-setup/templates/setup-audit.md: AI setup audit

## Commands by folder
- code-review/: /review
- coaching/: /kata
- delivery/: /spec, /orchestrate, /add-tracking, /cleanup-audit

## Rules
- Scan every skill, agent, command and tool setting with SkillSpector
  before committing: make check && make scan
- Never delete. Retired items go to _archive/<date>/.
- Don't load anything from _archive/.

## Plumbing (only when changing the library itself)
install, Makefile, scripts/, .claude-plugin/, .github/
