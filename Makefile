# =============================================================================
# Makefile commands
# =============================================================================

include .envs/docs

include tools/make/app.mk
include tools/make/code-quality.mk
include tools/make/docs.mk
include tools/make/docker.mk

HELP_FORMAT := %-25s %s\n

# Help
# ====

help:
	@echo "=================================================================="
	@echo "Makefile commands help"
	@echo "=================================================================="
	@echo ""
	@printf "$(HELP_FORMAT)" "help-app"				"Show help for project commands"
	@printf "$(HELP_FORMAT)" "help-code-quality"	"Show help for code quality commands"
	@printf "$(HELP_FORMAT)" "docker-help"    		"Show help for docker commands"
	@printf "$(HELP_FORMAT)" ""    ""


help-all:
	@echo ""
	@echo "All Makefile commands help"
	@$(MAKE) --no-print-directory help-app
	@$(MAKE) --no-print-directory help-code-quality
	@$(MAKE) --no-print-directory help-docker
