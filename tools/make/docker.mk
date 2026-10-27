# =============================================================================
# Docker commands
# =============================================================================

NAME := ds-bff
DOCKER_FILE := docker/Dockerfile


# Images
# ======

docker-build: ## Build the Docker image
	docker build -f $(DOCKER_FILE) -t $(NAME) .

docker-run: ## Create and start a new container (foreground, removed on stop)
	docker run --rm -p 9000:9000 --name $(NAME) $(NAME):latest

docker-stop: ## Stop and remove the container (if running)
	-docker rm -f $(NAME)

docker-recreate: docker-stop docker-build docker-run ## Rebuild image and recreate container on it

docker-logs: ## Show container logs in real time
	docker logs -f $(NAME)


# Help
# ====

HELP_FORMAT := %-25s %s\n

help-docker: ## Show help for Docker commands
	@echo ""
	@echo "=================================================================="
	@echo "Docker commands help"
	@echo "=================================================================="
	@echo ""
	@printf "$(HELP_FORMAT)" "docker-build"    "Build the Docker image"
	@echo ""
	@printf "$(HELP_FORMAT)" "docker-run"      "Create and start a new container (foreground, removed on stop)"
	@echo ""
	@printf "$(HELP_FORMAT)" "docker-recreate" "Rebuild image and recreate container on it"
	@echo ""
	@printf "$(HELP_FORMAT)" "docker-stop"     "Stop and remove the container (if running)"
	@echo ""
	@printf "$(HELP_FORMAT)" "docker-logs"     "Show container logs in real time"
	@echo ""