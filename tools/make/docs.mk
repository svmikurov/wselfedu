# =============================================================================
# Documentation commands
# =============================================================================

docs-docker-build: ## Build documentation image
	docker build -f docker/docs/Dockerfile -t wse-docs .

docs-docker-run: ## Run documentation server on http://localhost:$(DOCS_PORT)
	@echo "Running documentation image..."
	-@docker rm -f wse-docs
	docker run --rm -d \
		-p $(DOCS_PORT):8000 \
		-v "$(PWD)/docs/source:/docs/source" \
		--name wse-docs wse-docs
	@echo "🌐 Container started. Docs: http://localhost:$(DOCS_PORT)"

docs-docker-stop: ## Stop documentation server
	-docker stop wse-docs

# Help
# ====

help-docs-docker:
	@echo ""
	@echo "=================================================================="
	@echo "Documentation commands"
	@echo "=================================================================="
	@echo ""
	@printf "$(HELP_FORMAT)" "docs-docker-build" "Build documentation image"
	@echo ""
	@printf "$(HELP_FORMAT)" "docs-docker-run"   "Run documentation server on http://localhost:$(DOCS_PORT)"
	@echo ""
	@printf "$(HELP_FORMAT)" "docs-docker-stop"  "Stop documentation server"
	@echo ""