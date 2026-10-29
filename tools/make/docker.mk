# =============================================================================
# Docker compose commands
# =============================================================================

DC := docker compose -f docker-compose.django-orm.yml

# --- Secrets -----------------------------------------------------------------

compose-add-secrets:  # Generate ./secrets/* from .envs/*.secrets example
	@mkdir -p secrets
	@set -a; . ./.envs/db.secrets; set +a; \
		printf '%s' "$$DATABASE_PASSWORD" > secrets/database-password
	@echo "Wrote secrets/database-password"

# --- Stack lifecycle ---------------------------------------------------------

compose-build:  # Build images without starting
	$(DC) build

compose-up:  # Build image and start stack in background
	$(DC) up -d --build

compose-down:  # Stop and remove containers and network (DB volume kept)
	$(DC) down

compose-restart:  # Restart application container
	$(DC) restart wse-django-admin

compose-ps:  # Show status of project containers
	$(DC) ps

# --- Logs --------------------------------------------------------------------

compose-logs:  # Follow application logs in real time
	$(DC) logs -f --tail=100 wse-django-admin

compose-logs-db:  # Follow Postgres logs in real time
	$(DC) logs -f --tail=100 wse-postgres

# --- Migrations --------------------------------------------------------------

compose-migrate:  # Apply Django migrations (dev)
	$(DC) exec wse-django-admin python manage.py migrate

compose-migrate-plan:  # Show migration plan without applying (dev)
	$(DC) exec wse-django-admin python manage.py migrate --plan

compose-makemigrations:  # Generate new migrations from model changes (dev)
	$(DC) exec wse-django-admin python manage.py makemigrations

# --- Help --------------------------------------------------------------------

compose-help:
	@echo ""
	@echo "=================================================================="
	@echo "Docker compose recipes help"
	@echo "=================================================================="
	@echo ""
	@printf "$(HELP_FORMAT)" "compose-add-secrets"		"Generate ./secrets/* from .envs/*.secrets example"
	@echo ""
	@printf "$(HELP_FORMAT)" "compose-build"			"Build images without starting"
	@echo ""
	@printf "$(HELP_FORMAT)" "compose-up"				"Build image and start stack in background"
	@echo ""
	@printf "$(HELP_FORMAT)" "compose-down"				"Stop and remove containers and network"
	@echo ""
	@printf "$(HELP_FORMAT)" "compose-restart"			"Restart application container"
	@echo ""
	@printf "$(HELP_FORMAT)" "compose-ps"				"Show status of project containers"
	@echo ""
	@printf "$(HELP_FORMAT)" "compose-logs"				"Follow application logs"
	@echo ""
	@printf "$(HELP_FORMAT)" "compose-logs-db"			"Follow Postgres logs"
	@echo ""
	@printf "$(HELP_FORMAT)" "compose-migrate"			"Apply Django migrations (dev)"
	@echo ""
	@printf "$(HELP_FORMAT)" "compose-migrate-plan"		"Show migration plan without applying"
	@echo ""
	@printf "$(HELP_FORMAT)" "compose-makemigrations"	"Generate new migrations from models"
	@echo ""