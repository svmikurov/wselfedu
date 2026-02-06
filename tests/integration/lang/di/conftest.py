"""Translation presentation test configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from apps.core import models as core_models
from apps.core.di.configuration import ExerciseConfig
from apps.core.domain.exercise.presentation import (
    PresentationDomain,
)
from apps.core.handlers.protocols import (
    BusinessService,
    RegularValidator,
    ResponseAdapter,
)
from apps.lang import di, models, repositories, services
from di import MainContainer
from tests.fixtures.lang.no_db import translations as fixtures
from tests.fixtures.lang.no_db.presentation import EMPTY_PARAMETERS_DTO

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from apps.lang.handlers.presentation import WebPresentationUseCase
    from apps.users.models import Person

    # Dependency types
    # TODO: Update with abstract classes after adding them
    type Container = di.LanguageContainer
    type WebUseCase = WebPresentationUseCase
    type Repository = repositories.TranslationConditionsRepository
    type Service = services.PresentationService

    # Data types
    type Translations = list[models.EnglishTranslation]
    type Categories = list[models.Category]
    type Sources = list[core_models.Source]
    type Marks = list[models.Mark]
    type TranslationsQuerySet = QuerySet[models.EnglishTranslation]

# -----------------
# Mock dependencies
# -----------------


@pytest.fixture
def mock_validator() -> Mock:
    """Provide validator mock."""
    return Mock(spec=RegularValidator)


@pytest.fixture
def mock_service() -> Mock:
    """Provide business service mock."""
    return Mock(spec=BusinessService)


@pytest.fixture
def mock_response_adapter() -> Mock:
    """Provide response adapter mock."""
    return Mock(spec=ResponseAdapter)


# ------------
# Dependencies
# ------------


@pytest.fixture
def presentation_domain(
    exercise_configuration: ExerciseConfig,
) -> PresentationDomain:
    """Provide presentation domain."""
    return PresentationDomain(
        config=exercise_configuration,  # type: ignore
    )


@pytest.fixture
def repository() -> repositories.TranslationConditionsRepository:
    """Provide presentation repository."""
    return repositories.TranslationConditionsRepository(
        models.EnglishTranslation.objects
    )


# ------------
# DI container
# ------------


@pytest.fixture
def container() -> Container:
    """Provide presentation use case container."""
    return MainContainer.lang()


@pytest.fixture
def service(container: Container) -> Service:
    """Provide presentation service."""
    return container.exercise_service()  # type: ignore[no-any-return]


# DEPRECATED: Delete
@pytest.fixture
def web_use_case() -> WebUseCase:
    """Provide web use case."""
    return MainContainer.lang.view_container.web_regular_presentation()  # type: ignore[no-any-return, attr-defined]


# ----------------------
# Database data fixtures
# ----------------------


@pytest.fixture
def categories(user: Person) -> Categories:
    """Provide added to DB translation categories."""
    category_objs = [
        models.Category(user=user, name=name) for name in fixtures.CATEGORIES
    ]
    models.Category.objects.bulk_create(category_objs)
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
    marks_objs = [models.Mark(user=user, name=name) for name in fixtures.MARKS]
    models.Mark.objects.bulk_create(marks_objs)
    return marks_objs


@pytest.fixture
def translations_queryset(
    user: Person,
    repository: Repository,
    translations: Translations,  # Populate DB
) -> TranslationsQuerySet:
    """Provide translations queryset."""
    return repository.fetch(user, EMPTY_PARAMETERS_DTO)
