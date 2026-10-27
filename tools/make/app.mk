# =============================================================================
# Project commands
# =============================================================================

setup: ## Install project with dependencies
	poetry install

clean: ## Remove cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true

run-flask:  ## Run application via Flask entrypoint
	@poetry run flask --app src/wse/entrypoints/flask_app/app.py run --port 5005 --debug

# Help
# ====

help-app:
	@echo ""
	@echo "=================================================================="
	@echo "Project commands"
	@echo "=================================================================="
	@echo ""
	@printf "$(HELP_FORMAT)" "setup"		"Install project with dependencies"
	@echo ""
	@printf "$(HELP_FORMAT)" "run-flask"	"Run application via Flask entrypoint"
	@echo ""
	@printf "$(HELP_FORMAT)" "clean"		"Remove cache files"
	@printf "$(HELP_FORMAT)" ""		""