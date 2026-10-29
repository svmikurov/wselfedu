# =============================================================================
# Makefile commands
# =============================================================================

include .envs/docs

include tools/make/app.mk
include tools/make/code-quality.mk
include tools/make/docs.mk
include tools/make/docker.mk

HELP_FORMAT =   \033[36m%-30s\033[0m %s\n

# Help
# ====

help:
	@echo "=================================================================="
	@echo "Makefile commands help"
	@echo "=================================================================="
	@echo ""
	@printf "$(HELP_FORMAT)" "help-app"				"Show help for project commands"
	@echo ""
	@printf "$(HELP_FORMAT)" "help-code-quality"	"Show help for code quality commands"
	@echo ""
	@printf "$(HELP_FORMAT)" "compose-help"    		"Show help for docker commands"
	@echo ""


help-all:
	@echo ""
	@echo "All Makefile commands help"
	@$(MAKE) --no-print-directory help-app
	@$(MAKE) --no-print-directory help-code-quality
	@$(MAKE) --no-print-directory compose-help
