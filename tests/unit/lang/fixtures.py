"""Language discipline fixtures."""

import uuid
from unittest.mock import Mock

import pytest

from apps.core.storage.clients import DjangoCache
from apps.lang import models, schemas, services, types
from apps.lang.repos.abc import ProgressABC
from apps.users.models import CustomUser

from .api.v1.study import cases

# Data fixtures
# -------------


@pytest.fixture
def case_uuid() -> uuid.UUID:
    """Provide Word study presentation case."""
    return uuid.UUID('5b518a3e-45a4-4147-a097-0ed28211d8a4')


@pytest.fixture
def presentation() -> types.PresentationDataT:
    """Provide presentation data."""
    return {
        'definition': 'house',
        'explanation': 'дом',
        'info': {'progress': 7},
    }


@pytest.fixture
def presentation_case(
    case_uuid: uuid.UUID,
    presentation: types.PresentationDataT,
) -> types.PresentationCaseT:
    """Provide Word study presentation case."""
    return {'case_uuid': case_uuid, **presentation}


@pytest.fixture
def stored_case() -> schemas.WordStudyStoredCase:
    """Provide Word study case data."""
    return schemas.WordStudyStoredCase(
        translation_id=1,
        language='english',
    )


@pytest.fixture
def progress_config() -> schemas.ProgressConfigSchema:
    """Word study progress config schema."""
    return schemas.ProgressConfigSchema(
        increment=1,
        decrement=1,
    )


@pytest.fixture
def progress_case() -> types.WordProgressT:
    """Provide valid word study progress update case."""
    return cases.VALID_PAYLOAD


# Database fixtures
# -----------------


@pytest.fixture
def native_word(
    user: CustomUser,
    presentation: types.PresentationT,
) -> models.NativeWord:
    """Native word fixture."""
    return models.NativeWord.objects.create(
        user=user,
        word=presentation['explanation'],
    )


@pytest.fixture
def english_word(
    user: CustomUser,
    presentation: types.PresentationT,
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
    presentation: types.PresentationT,
    translation: models.EnglishTranslation,
) -> models.EnglishProgress:
    """Get translation fixture."""
    return models.EnglishProgress.objects.create(
        user=user,
        translation=translation,
        progress=presentation['info']['progress'],  # type: ignore[typeddict-item]
    )


# Mocked dependency fixtures
# --------------------------


@pytest.fixture
def mock_progress_repo() -> Mock:
    """Mock Word study progress repo fixture."""
    return Mock(spec=ProgressABC)


@pytest.fixture
def mock_django_cache_storage(
    case_uuid: uuid.UUID,
) -> Mock:
    """Mock Django cache storage fixture."""
    mock = Mock(spec=DjangoCache)
    mock.set.return_value = case_uuid
    return mock


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
