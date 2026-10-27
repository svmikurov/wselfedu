# =============================================================================
# Code quality commands
# =============================================================================

# Linter commands
# ===============

lint: ## Check code style (read-only)
	poetry run ruff check

fix: ## Auto-fix lint issues
	poetry run ruff check --fix

format: ## Format code with ruff
	poetry run ruff format


# Type check commands
# ===================

type-check: ## Check types with mypy
	poetry run mypy .


# Test commands
# =============

test: ## Run tests
	poetry run pytest -v


# Combined check commands
# =======================

ci: lint type-check test ## CI check (read-only: lint + type-check + test)

check-code: format fix type-check ## Check code (format + fix + type-check)

check: check-code test ## Full check (format + fix + type-check + test)


# Help
# ====

help-code-quality:
	@echo ""
	@echo "=================================================================="
	@echo "Code quality commands"
	@echo "=================================================================="
	@echo ""
	@echo "Linter commands"
	@echo "==============="
	@printf "$(HELP_FORMAT)" "lint"        "Check code style (read-only)"
	@printf "$(HELP_FORMAT)" "fix"         "Auto-fix lint issues"
	@printf "$(HELP_FORMAT)" "format"      "Format code with ruff"
	@echo ""
	@echo "Type check commands"
	@echo "==================="
	@printf "$(HELP_FORMAT)" "type-check"  "Check types with mypy"
	@echo ""
	@echo "Test commands"
	@echo "============="
	@printf "$(HELP_FORMAT)" "test"        "Run tests"
	@echo ""
	@echo "Combined check commands"
	@echo "======================="
	@printf "$(HELP_FORMAT)" "ci"          "CI check (read-only: lint + type-check + test)"
	@printf "$(HELP_FORMAT)" "check"       "Full check (format + fix + type-check + test)"
	@printf "$(HELP_FORMAT)" "check-code"  "Check code (format + fix + type-check) without tests"
	@echo ""