"""Word study Presentation repository test."""

from datetime import timedelta

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

from apps.core import models as models_core
from apps.lang import models, repos, types
from apps.users.models import Person
from tests.fixtures.lang.no_db import translation_query as fixtures


@pytest.fixture
def conditions() -> types.WordParameters:
    """Provide Word study lookup empty conditions."""
    return fixtures.EMPTY_LOOKUP_CONDITIONS.copy()


class TestGetByStartPeriod:
    """Fetch translations by start period conditions."""

    # TODO: Implement edge periods validation?
    @pytest.mark.django_db
    def test_filter_when_end_older_that_start_edge(
        self,
        presentation_repo: repos.EnglishPresentation,
        conditions: types.WordParameters,
    ) -> None:
        """Repository correctly fetch data when end older start."""
        # Arrange
        conditions['start_period'] = types.IdName(id=2, name='yesterday')
        conditions['end_period'] = types.IdName(id=4, name='three days age')

        # Act
        candidates = presentation_repo.get_candidates(conditions)

        # Assert
        assert () == tuple(*candidates)

    def test_filter_bad_edge_period(
        self,
        presentation_repo: repos.EnglishPresentation,
        conditions: types.WordParameters,
    ) -> None:
        """Repository correctly fetch data by bad edge period."""
        # Arrange
        conditions['start_period'] = types.IdName(id=0, name='bad')

        # Act & Assert
        with pytest.raises(KeyError):
            presentation_repo.get_candidates(conditions)

    @pytest.mark.django_db
    def test_filter_edge_period(
        self,
        presentation_repo: repos.EnglishPresentation,
        translations: list[models.EnglishTranslation],
        conditions: types.WordParameters,
    ) -> None:
        """Repository correctly fetch data by edge periods."""
        today = timezone.now()

        # Arrange
        # - Set date
        translations[1].created_at = today - timedelta(days=1)
        translations[2].created_at = today - timedelta(days=2)
        translations[3].created_at = today - timedelta(days=3)
        translations[4].created_at = today - timedelta(days=4)

        # - Update translation created at
        models.EnglishTranslation.objects.bulk_update(
            translations, ['created_at']
        )

        # - Set lookup conditions
        conditions['start_period'] = types.IdName(id=4, name='three days ago')
        conditions['end_period'] = types.IdName(id=2, name='yesterday')

        # Act
        candidates = presentation_repo.get_candidates(conditions)

        # Assert
        assert (
            # not include 'today'
            translations[1].pk,  # include start edge ('yesterday')
            translations[2].pk,  # include inner data
            translations[3].pk,  # include end edge ('three days ago')
            # not include 'four days ago'
        ) == tuple(*candidates)

    @pytest.mark.django_db
    def test_filter_by_better_period(
        self,
        presentation_repo: repos.EnglishPresentation,
        translations: list[models.EnglishTranslation],
        conditions: types.WordParameters,
    ) -> None:
        """Repository correctly fetch data by better period."""
        # Arrange
        conditions['start_period'] = types.IdName(id=6, name='week ago')

        # Act
        candidates = presentation_repo.get_candidates(conditions)

        # Assert
        assert [item.pk for item in translations] == list(*candidates)

    @pytest.mark.django_db
    def test_filter_by_start_today(
        self,
        presentation_repo: repos.EnglishPresentation,
        translations: list[models.EnglishTranslation],
        conditions: types.WordParameters,
    ) -> None:
        """Repository correctly fetch data by start period 'today'."""
        # Arrange
        conditions['start_period'] = types.IdName(id=1, name='today')

        # Act
        candidates = presentation_repo.get_candidates(conditions)

        # Assert
        assert [item.pk for item in translations] == list(*candidates)


class TestGetByRelationships:
    """Fetch translations by relationship conditions."""

    @pytest.mark.django_db
    def test_fetch_candidates_by_relationship(
        self,
        presentation_repo: repos.EnglishPresentation,
        translations: list[models.EnglishTranslation],
        translations_meta: tuple[
            list[models.LangCategory],
            list[models_core.Source],
            list[models.LangMark],
        ],
        conditions: types.WordParameters,
    ) -> None:
        """Repository correctly fetch data by relationship."""
        categories, sources, marks = translations_meta

        # Arrange
        desired_category = categories[0]
        desired_mark = marks[0]
        desired_source = sources[1]

        other_category = categories[1]
        other_mark = marks[1]
        other_source = sources[0]

        # - Configure translation model objects
        translations[0].category = desired_category  # Valid case
        translations[2].category = desired_category  # Valid case
        translations[5].category = other_category
        translations[6].category = desired_category
        translations[7].category = desired_category

        translations[0].source = desired_source  # Valid case
        translations[2].source = desired_source  # Valid case
        translations[5].source = desired_source
        translations[6].source = other_source
        translations[7].source = desired_source

        translations[0].marks.add(desired_mark)  # Valid case
        translations[2].marks.add(desired_mark)  # Valid case
        translations[5].marks.add(desired_mark)
        translations[6].marks.add(desired_mark)
        translations[7].marks.add(other_mark)

        # - Update translation meta DB data
        models.EnglishTranslation.objects.bulk_update(
            translations, ['category', 'source']
        )

        # - Word study lookup conditions
        conditions['category'] = types.IdName(id=desired_category.pk, name='')
        conditions['mark'] = types.IdName(id=desired_mark.pk, name='')
        conditions['word_source'] = types.IdName(id=desired_source.pk, name='')

        # Act
        candidates = presentation_repo.get_candidates(conditions)

        # Assert
        # - Got translations only with desired category, mark and source
        assert (
            translations[0].pk,
            translations[2].pk,
        ) == tuple(*candidates)

    @pytest.mark.django_db
    def test_not_parameters_success(
        self,
        presentation_repo: repos.EnglishPresentation,
        translations: list[models.EnglishTranslation],
        conditions: types.WordParameters,
    ) -> None:
        """Repository correctly fetch valid data from DB."""
        # Act
        # - All presentation parameters has None value
        candidates = presentation_repo.get_candidates(conditions)

        # Assert
        # - Got all translations
        assert [item.pk for item in translations] == list(*candidates)


@pytest.mark.django_db
class TestGetWordByTranslation:
    """Get word by translation to study tests."""

    def test_get_word_study_data_success(
        self,
        user: Person,
        word_translation: models.EnglishTranslation,
        native_word: models.NativeWord,
        english_word: models.EnglishWord,
        english_progress: models.EnglishProgress,  # Adds progress to DB
        presentation_repo: repos.EnglishPresentation,
    ) -> None:
        """Test get Word study case data by translation ID."""
        # Act
        result = presentation_repo.get_word_study_data(
            user=user,
            translation_id=word_translation.pk,
            language='english',
        )

        # Assert
        assert result['definition'] == english_word.word
        assert result['explanation'] == native_word.word
        assert result['info']['progress'] == english_progress.progress
        assert len(result) == 3

    def get_word_study_data_not_found(
        self,
        presentation_repo: repos.EnglishPresentation,
        user: Person,
    ) -> None:
        """Test case when translation doesn't exist."""
        # Arrange
        no_exist_translation_id = 999

        # Act & Assert
        with pytest.raises(ObjectDoesNotExist):
            presentation_repo.get_word_study_data(
                user=user,
                translation_id=no_exist_translation_id,
                language='english',
            )

    def get_word_study_data_other_users(
        self,
        presentation_repo: repos.EnglishPresentation,
        user_not_owner: Person,
        word_translation: models.EnglishTranslation,
    ) -> None:
        """Test that users can only access their own translations."""
        # Act & Assert - other user shouldn't see the translation
        with pytest.raises(ObjectDoesNotExist):
            presentation_repo.get_word_study_data(
                user=user_not_owner,
                translation_id=word_translation.pk,
                language='english',
            )

    def get_word_study_data_query_count(
        self,
        presentation_repo: repos.EnglishPresentation,
        user: Person,
        word_translation: models.EnglishTranslation,
        django_assert_num_queries: CaptureQueriesContext,
    ) -> None:
        """Test that only one query is executed."""
        # Act & Assert
        with django_assert_num_queries(1):  # type: ignore[operator]
            presentation_repo.get_word_study_data(
                user=user,
                translation_id=word_translation.pk,
                language='english',
            )
