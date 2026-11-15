.PHONY: install scan external uninstall check hooks

install: ## Install plugin + default MCP servers into Claude Code
	./install

scan: ## Run SkillSpector over skills, agents, commands and MCP config (commit gate)
	./install --scan

external: ## Menu of optional third-party tools
	./install --external

uninstall:
	./install --uninstall

check: ## Validate JSON + skill frontmatter without network
	python3 -I scripts/check.py

hooks: ## Install the git pre-commit hook that runs scan + check
	ln -sf ../../scripts/pre-commit .git/hooks/pre-commit && echo "pre-commit hook installed"
