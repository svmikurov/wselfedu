# =============================================================================
# INFRASTURCTURE
# =============================================================================

run-django-orm:  ## Run Docker Compose with a build Django ORM admin
	docker compose -f docker-compose.dev.django_orm.yml up --build

rebuild-django-orm:  ## Rebuild Docker Compose with a clean Django ORM admin
	docker compose -f docker-compose.dev.django_orm.yml down -v || true
	docker rmi wse-django-orm wse-postgres 2>/dev/null || true
	docker builder prune -f || true
	docker compose -f docker-compose.dev.django_orm.yml up --build