# =============================================================================
# DOCUMENTATION
# =============================================================================

.PHONY: docs-build docs-run docs-stop docs-clean

DOCS_IMAGE_NAME = wse-docs
DOCS_CONTAINER_NAME = wse-docs
DOCS_HOST ?= 8010

docs-build:  ## Build documentation Docker image
	docker build -f docker/docs/Dockerfile -t $(DOCS_IMAGE_NAME) .

docs-run: docs-build  ## Build and run documentation Docker container
	docker rm -f $(DOCS_CONTAINER_NAME) 2>/dev/null || true
	docker run -d -p $(DOCS_HOST):8000 --name $(DOCS_CONTAINER_NAME) $(DOCS_IMAGE_NAME)
	@echo "🌐 Documentation: http://localhost:$(DOCS_HOST)"
	@echo ""

docs-stop:  ## Stop documentation Docker container
	docker stop $(DOCS_CONTAINER_NAME) 2>/dev/null || true

docs-clean: docs-stop  ## Remove documentation Docker image and container
	docker rm $(DOCS_CONTAINER_NAME) 2>/dev/null || true
	docker rmi $(DOCS_IMAGE_NAME) 2>/dev/null || true