# =============================================================================
# INFRASTRUCTURE
# =============================================================================

# Docker commands
# ~~~~~~~~~~~~~~~

run-django-orm:  ## Run Docker Compose with a build Django ORM admin
	docker compose -f docker-compose.dev.django_orm.yml up --build

rebuild-django-orm:  ## Rebuild Docker Compose with a clean Django ORM admin
	docker compose -f docker-compose.dev.django_orm.yml down -v || true
	docker rmi wse-django-orm wse-postgres 2>/dev/null || true
	docker builder prune -f || true
	docker compose -f docker-compose.dev.django_orm.yml up --build

# Socket commands
# ~~~~~~~~~~~~~~~

run-socket-server:  ## Run socket server example
	poetry run python3 src/wse/infrastructure/endpoints/server.py

run-socket-client:  ## Run socket client example
	poetry run python3 src/wse/infrastructure/endpoints/client.py

help-infra:
	@echo "=============================================="
	@echo "Infrastructure layer development Make commands"
	@echo "=============================================="
	@echo ""
	@echo "Docker commands"
	@echo "~~~~~~~~~~~~~~~"
	@echo "run-django-orm 		- Run docker compose with build Django ORM administration"
	@echo "rebuild-django-orm	- Rebuild docker compose with clean Django ORM administration"
	@echo ""
	@echo "Socket commands"
	@echo "~~~~~~~~~~~~~~~"
	@echo "run-socket-server	- Run socket *server* example"
	@echo "run-socket-client	- Run socket *client* example"