"""Word study Presentation parameters Repository tests."""

import pytest
from django.test.utils import CaptureQueriesContext

from apps.lang import repositories, types
from apps.users.models import Person
from tests.fixtures.lang.no_db import translations as fixtures

pytestmark = pytest.mark.django_db


class TestCreate:
    """Create presentation parameters tests."""

    def test_create_parameters_success(
        self,
        user: Person,
        parameters_repo: repositories.StudyParametersRepository,
    ) -> None:
        """Parameters was successfully created."""
        # Arrange
        user_parameters = fixtures.EMPTY_TRANSLATION_PARAMETERS.copy()
        user_parameters['word_count'] = 45

        # Act
        result = parameters_repo.update(user, user_parameters)

        # Assert
        assert result['word_count'] == user_parameters['word_count']


class TestFetch:
    """Fetch Word study Presentation params repository tests."""

    def test_fetch_public_parameters(
        self,
        user: Person,
        parameters_repo: repositories.StudyParametersRepository,
        public_parameters: types.CaseSettingsAPI,
    ) -> None:
        """Test fetch public default data."""
        # Act & assert
        assert public_parameters == parameters_repo.fetch(user)

    def test_fetch_data(
        self,
        user: Person,
        parameters_repo: repositories.StudyParametersRepository,
        parameters_db_data: types.CaseSettingsAPI,
        django_assert_num_queries: CaptureQueriesContext,
    ) -> None:
        """Test fetch initial data."""
        # Act & assert
        with django_assert_num_queries(7):  # type: ignore[operator]
            assert parameters_db_data == parameters_repo.fetch(user)


class TestUpdate:
    """Update Word study Presentation params repository tests."""

    def test_update_parameters(
        self,
        user: Person,
        parameters_repo: repositories.StudyParametersRepository,
        parameters_db_data: types.CaseSettingsAPI,
        django_assert_num_queries: CaptureQueriesContext,
    ) -> None:
        """Test update initial data."""
        # Arrange
        # - Select a parameter from the options
        # to set it as the initial value
        mark = parameters_db_data['marks'][1]

        # - Parameter data without option fields to update
        new_params = {
            key: parameters_db_data[key]  # type: ignore[literal-required]
            for key in parameters_db_data.keys()
            if key not in ('categories', 'marks', 'sources', 'periods')
        }
        new_params['mark'] = mark
        new_params['word_count'] = 76

        # - Expected new parameter data
        expected = parameters_db_data.copy()
        expected['mark'] = [mark]
        expected['word_count'] = 76

        # Act
        # TODO: Fix database query count
        with django_assert_num_queries(21):  # type: ignore[operator]
            updated_parameters = parameters_repo.update(user, new_params)  # type: ignore[arg-type]

        # Assert
        assert expected == updated_parameters

    def test_update_with_none(
        self,
        user: Person,
        parameters_repo: repositories.StudyParametersRepository,
        parameters_db_data: types.CaseSettingsAPI,
    ) -> None:
        """Test that updated parameter is None."""
        # Arrange
        update_data = {
            key: None
            for key in (
                'category',
                'mark',
                'word_source',
                'word_count',
                'start_period',
                'end_period',
                'question_timeout',
                'answer_timeout',
                'is_study',
                'is_repeat',
                'is_examine',
                'is_know',
            )
        }
        expected = {**parameters_db_data, **update_data}
        expected['is_study'] = True
        expected['is_repeat'] = True
        expected['is_examine'] = True
        expected['is_know'] = False

        # Act & Assert
        assert expected == parameters_repo.update(user, update_data)  # type: ignore[arg-type]
