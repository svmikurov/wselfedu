"""Language discipline fixtures."""

from unittest.mock import Mock

import pytest

from apps.core.storage.clients import DjangoCache
from apps.lang import models, schemas, services, types
from apps.lang.repos.abc import ProgressABC
from apps.users.models import CustomUser

from .api.v1.study import cases


@pytest.fixture
def mock_progress_repo() -> Mock:
    """Mock Word study progress repo fixture."""
    return Mock(spec=ProgressABC)


@pytest.fixture
def mock_django_cache_storage() -> Mock:
    """Mock Django cache storage fixture."""
    return Mock(spec=DjangoCache)


@pytest.fixture
def progress_config() -> schemas.ProgressConfigSchema:
    """Word study progress config schema."""
    return schemas.ProgressConfigSchema(
        increment=1,
        decrement=1,
    )


@pytest.fixture
def progress_service_di_mock(
    mock_progress_repo: Mock,
    mock_django_cache_storage: Mock,
    progress_config: schemas.ProgressConfigSchema,
) -> services.UpdateWordProgressService:
    """Test Word study progress update service."""
    return services.UpdateWordProgressService(
        progress_repo=mock_progress_repo,
        case_storage=mock_django_cache_storage,
        progress_config=progress_config,
    )


@pytest.fixture
def presentation() -> types.PresentationDict:
    """Provide presentation data."""
    return types.PresentationDict(
        definition='house',
        explanation='дом',
        progress=7,
    )


@pytest.fixture
def native_word(
    user: CustomUser,
    presentation: types.PresentationDict,
) -> models.NativeWord:
    """Native word fixture."""
    return models.NativeWord.objects.create(
        user=user,
        word=presentation['explanation'],
    )


@pytest.fixture
def english_word(
    user: CustomUser,
    presentation: types.PresentationDict,
) -> models.EnglishWord:
    """English word fixture."""
    return models.EnglishWord.objects.create(
        user=user,
        word=presentation['definition'],
    )


@pytest.fixture
def translation(
    user: CustomUser,
    native_word: models.NativeWord,
    english_word: models.EnglishWord,
) -> models.EnglishTranslation:
    """Get translation fixture."""
    return models.EnglishTranslation.objects.create(
        user=user, native=native_word, english=english_word
    )


@pytest.fixture
def english_progress(
    user: CustomUser,
    presentation: types.PresentationDict,
    translation: models.EnglishTranslation,
) -> models.EnglishProgress:
    """Get translation fixture."""
    return models.EnglishProgress.objects.create(
        user=user,
        translation=translation,
        progress=presentation['progress'],  # type: ignore[misc]
    )


@pytest.fixture
def progress_case() -> types.WordProgressType:
    """Provide valid word study progress update case."""
    return cases.VALID_PAYLOAD


@pytest.fixture
def case_data() -> schemas.WordStudyCaseSchema:
    """Provide Word study case data."""
    return schemas.WordStudyCaseSchema(
        translation_id=1,
        language='english',
    )
