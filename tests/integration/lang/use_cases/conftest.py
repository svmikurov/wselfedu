"""Translation presentation test configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from apps.core import models as core_models
from apps.lang import di, domain, models, repositories, services
from apps.lang.types import presentation
from tests.fixtures.lang.no_db import translations as fixtures
from tests.fixtures.lang.no_db.presentation import EMPTY_PARAMETERS_DTO

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from apps.lang import use_cases
    from apps.users.models import Person

    # Dependency types
    # TODO: Update with abstract classes after adding them
    type Container = di.PresentationContainer
    type WebUseCase = use_cases.WebPresentationUseCase
    type Repository = repositories.EnglishTranslation
    type Service = services.PresentationService

    # Data types
    type Translations = list[models.EnglishTranslation]
    type Categories = list[models.LangCategory]
    type Sources = list[core_models.Source]
    type Marks = list[models.LangMark]
    type TranslationsQuerySet = QuerySet[models.EnglishTranslation]

# -----------------
# Mock dependencies
# -----------------


@pytest.fixture
def mock_validator() -> Mock:
    """Provide validator mock."""
    return Mock(spec=presentation.Validator)


@pytest.fixture
def mock_service() -> Mock:
    """Provide business service mock."""
    return Mock(spec=presentation.BusinessService)


@pytest.fixture
def mock_response_adapter() -> Mock:
    """Provide response adapter mock."""
    return Mock(spec=presentation.ResponseAdapter)


# ------------
# Dependencies
# ------------


@pytest.fixture
def presentation_domain() -> domain.PresentationDomain:
    """Provide presentation domain."""
    return domain.PresentationDomain()


@pytest.fixture
def repository() -> repositories.EnglishTranslation:
    """Provide presentation repository."""
    return repositories.EnglishTranslation()


# ------------
# DI container
# ------------


@pytest.fixture
def container() -> Container:
    """Provide presentation use case container."""
    return di.PresentationContainer()


@pytest.fixture
def service(container: Container) -> Service:
    """Provide presentation service."""
    return container.eng_service()


@pytest.fixture
def web_use_case(container: Container) -> WebUseCase:
    """Provide web use case."""
    return container.web_use_case()


# ----------------------
# Database data fixtures
# ----------------------


@pytest.fixture
def categories(user: Person) -> Categories:
    """Provide added to DB translation categories."""
    category_objs = [
        models.LangCategory(user=user, name=name)
        for name in fixtures.CATEGORIES
    ]
    models.LangCategory.objects.bulk_create(category_objs)
    return category_objs


@pytest.fixture
def sources(user: Person) -> Sources:
    """Provide added to DB translation categories."""
    source_objs = [
        core_models.Source(user=user, name=name) for name in fixtures.SOURCES
    ]
    core_models.Source.objects.bulk_create(source_objs)
    return source_objs


@pytest.fixture
def marks(user: Person) -> Marks:
    """Provide added to DB translation categories."""
    marks_objs = [
        models.LangMark(user=user, name=name) for name in fixtures.MARKS
    ]
    models.LangMark.objects.bulk_create(marks_objs)
    return marks_objs


@pytest.fixture
def translations_queryset(
    user: Person,
    repository: Repository,
    translations: Translations,  # Populate DB
) -> TranslationsQuerySet:
    """Provide translations queryset."""
    return repository.fetch(user, EMPTY_PARAMETERS_DTO)
