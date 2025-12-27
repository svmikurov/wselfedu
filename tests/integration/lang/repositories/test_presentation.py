"""Translation presentation repository tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from apps.core import models as core_models
from apps.lang import models as lang_models
from apps.lang import repositories
from apps.lang.repositories import get_period_delta, presentation
from apps.study import models as study_models
from tests.fixtures.lang.no_db import translations as fixtures
from tests.fixtures.lang.no_db.presentation import EMPTY_PARAMETERS_DTO

if TYPE_CHECKING:
    from apps.users.models import Person

    type Repository = presentation.EnglishTranslation
    type Translations = list[lang_models.EnglishTranslation]
    type Categories = list[lang_models.LangCategory]
    type Sources = list[core_models.Source]
    type Marks = list[lang_models.LangMark]


@pytest.fixture
def sources(user: Person) -> Sources:
    """Provide added to DB translation categories."""
    source_objs = [
        core_models.Source(user=user, name=name) for name in fixtures.SOURCES
    ]
    core_models.Source.objects.bulk_create(source_objs)
    return source_objs


@pytest.fixture
def categories(user: Person) -> Categories:
    """Provide added to DB translation categories."""
    category_objs = [
        lang_models.LangCategory(user=user, name=name)
        for name in fixtures.CATEGORIES
    ]
    lang_models.LangCategory.objects.bulk_create(category_objs)
    return category_objs


@pytest.fixture
def marks(user: Person) -> Marks:
    """Provide added to DB translation categories."""
    marks_objs = [
        lang_models.LangMark(user=user, name=name) for name in fixtures.MARKS
    ]
    lang_models.LangMark.objects.bulk_create(marks_objs)
    return marks_objs


@pytest.fixture
def repository() -> repositories.EnglishTranslation:
    """Provide presentation repository."""
    return repositories.EnglishTranslation()


class TestProgressFilter:
    """Presentation repository period filter tests."""

    @pytest.mark.django_db
    def test_exclude_any_phases(
        self,
        repository: Repository,
        user: Person,
        translations: Translations,  # Populate DB
    ) -> None:
        """Exclude any progress phases."""
        # Arrange
        # - Set progress
        repeat_translation = translations[0]
        known_translation = translations[1]

        repeat_translation.progress = study_models.Progress.REPEAT_DEFAULT
        known_translation.progress = study_models.Progress.KNOW_DEFAULT
        repeat_translation.save()
        known_translation.save()

        # - Set condition
        conditions = EMPTY_PARAMETERS_DTO.model_copy(
            update={'is_repeat': False, 'is_know': False}
        )

        # Act
        result = repository.fetch(user, conditions)

        # Assert
        # - Exclude translations with progress
        assert result.count() == len(translations) - 2
        assert repeat_translation not in result
        assert known_translation not in result


class TestPeriodFilter:
    """Presentation repository period filter tests."""

    @pytest.mark.django_db
    def test_bad_period(
        self,
        repository: Repository,
        user: Person,
        translations: Translations,  # Populate DB
    ) -> None:
        """Bad period."""
        # Today period id = 1
        # Bad date, end period is greater than start period
        end_period_id = 2
        start_period_id = 1
        older_period_id = 4

        # Arrange
        # - Set date
        translations[1].created_at = get_period_delta(end_period_id)
        translations[2].created_at = get_period_delta(start_period_id)
        translations[3].created_at = get_period_delta(older_period_id)

        translations[1].save()
        translations[2].save()
        translations[3].save()

        # - Set condition
        conditions = EMPTY_PARAMETERS_DTO.model_copy(
            update={
                'start_period': start_period_id,
                'end_period': end_period_id,
            }
        )

        # Act
        result = repository.fetch(user, conditions)

        # Assert
        assert result.count() == 0

    @pytest.mark.django_db
    def test_middle_period(
        self,
        repository: Repository,
        user: Person,
        translations: Translations,  # Populate DB
    ) -> None:
        """End period older start."""
        # Today period id = 1
        end_period_id = 2
        start_period_id = 3
        older_period_id = 4

        # Arrange
        # - Set date
        translations[1].created_at = get_period_delta(end_period_id)
        translations[2].created_at = get_period_delta(start_period_id)
        translations[3].created_at = get_period_delta(older_period_id)

        translations[1].save()
        translations[2].save()
        translations[3].save()

        # - Set condition
        conditions = EMPTY_PARAMETERS_DTO.model_copy(
            update={
                'start_period': start_period_id,
                'end_period': end_period_id,
            }
        )

        # Act
        result = repository.fetch(user, conditions)

        # Assert
        assert result.count() == 2
        assert translations[1] in result
        assert translations[2] in result


class TestRelationshipFilter:
    """Presentation repository relationship filter tests."""

    @pytest.mark.django_db
    def test_filter_by_any_marks(
        self,
        repository: Repository,
        user: Person,
        translations: Translations,  # Populate DB
        marks: Marks,  # Populate DB
    ) -> None:
        """Filter a translations by any marks."""
        # Arrange
        # - Select ORM model objects
        mark_1 = marks[0]
        mark_2 = marks[1]
        mark_3 = marks[2]

        translation_1 = translations[0]
        translation_2 = translations[2]
        translation_3 = translations[3]

        # - Create ORM model object relationships
        translation_1.marks.add(mark_1)
        translation_2.marks.add(mark_1, mark_3)
        translation_3.marks.add(mark_2, mark_3)
        translation_1.save()
        translation_2.save()
        translation_3.save()

        # - Set condition
        conditions = EMPTY_PARAMETERS_DTO.model_copy(
            update={'mark': [mark_2.pk, mark_3.pk]}
        )

        # Act
        result = repository.fetch(user, conditions)

        # Assert
        assert result.count() == 2
        assert translation_1 not in result
        assert translation_2 in result
        assert translation_3 in result

    @pytest.mark.django_db
    def test_filter_by_one_mark(
        self,
        repository: Repository,
        user: Person,
        translations: Translations,  # Populate DB
        marks: Marks,  # Populate DB
    ) -> None:
        """Filter a translations by one mark."""
        # Arrange
        # - Select ORM model objects
        mark_1 = marks[0]
        mark_2 = marks[1]
        mark_3 = marks[2]

        translation_1 = translations[0]
        translation_2 = translations[2]
        translation_3 = translations[3]

        # - Create ORM model object relationships
        translation_1.marks.add(mark_1)
        translation_2.marks.add(mark_1, mark_3)
        translation_3.marks.add(mark_2, mark_3)
        translation_1.save()
        translation_2.save()
        translation_3.save()

        # - Set condition
        conditions = EMPTY_PARAMETERS_DTO.model_copy(
            update={'mark': [mark_2.pk]}
        )

        # Act
        result = repository.fetch(user, conditions)

        # Assert
        assert result.count() == 1
        assert translation_1 not in result
        assert translation_2 not in result
        assert translation_3 in result

    @pytest.mark.django_db
    def test_filter_by_source(
        self,
        repository: Repository,
        user: Person,
        translations: Translations,  # Populate DB
        sources: Sources,  # Populate DB
    ) -> None:
        """Filter a translations by source."""
        # Arrange
        # - Select ORM model objects
        source_1 = sources[0]  # Valid category
        source_2 = sources[1]
        translation_1 = translations[2]  # Valid translation
        translation_2 = translations[3]
        translation_3 = translations[4]  # Valid translation

        # - Create ORM model object relationships
        translation_1.source = source_1
        translation_2.source = source_2
        translation_3.source = source_1
        translation_1.save()
        translation_2.save()
        translation_3.save()

        # - Set condition
        conditions = EMPTY_PARAMETERS_DTO.model_copy(
            update={'source': source_1.pk}
        )

        # Act
        result = repository.fetch(user, conditions)

        # Assert
        assert result.count() == 2
        assert translation_1 in result
        assert translation_2 not in result
        assert translation_3 in result

    @pytest.mark.django_db
    def test_filter_by_category(
        self,
        repository: Repository,
        user: Person,
        translations: Translations,  # Populate DB
        categories: Categories,  # Populate DB
    ) -> None:
        """Filter a translations by category."""
        # Arrange
        # - Select ORM model objects
        category_1 = categories[0]  # Valid category
        category_2 = categories[1]
        translation_1 = translations[0]  # Valid translation
        translation_2 = translations[4]
        translation_3 = translations[5]  # Valid translation

        # - Create ORM model object relationships
        translation_1.category = category_1
        translation_2.category = category_2
        translation_3.category = category_1
        translation_1.save()
        translation_2.save()
        translation_3.save()

        # - Set condition
        conditions = EMPTY_PARAMETERS_DTO.model_copy(
            update={'category': category_1.pk}
        )

        # Act
        result = repository.fetch(user, conditions)

        # Assert
        assert result.count() == 2
        assert translation_1 in result
        assert translation_2 not in result
        assert translation_3 in result

    @pytest.mark.django_db
    def test_no_filters(
        self,
        repository: Repository,
        user: Person,
        translations: Translations,  # Populate DB
    ) -> None:
        """Fetch all translations if no request conditions."""
        # Act
        result = repository.fetch(user, EMPTY_PARAMETERS_DTO)

        # Assert
        assert result.count() == len(translations)

    @pytest.mark.django_db
    def test_no_translations(
        self,
        repository: Repository,
        user: Person,
    ) -> None:
        """User have no translations."""
        assert repository.fetch(user, EMPTY_PARAMETERS_DTO).count() == 0


class TestCreateRepository:
    """Translation presentation repository create tests."""

    def test_create_repository(self) -> None:
        """Create repository."""
        assert presentation.EnglishTranslation() is not None
