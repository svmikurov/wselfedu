"""Word study presentation service tests."""

import pytest

from apps.core import exceptions
from apps.core import models as models_core
from apps.lang import models, services, types
from apps.users.models import Person


class TestGetPresentationCase:
    """Get Word study presentation case tests."""

    @pytest.mark.django_db
    def test_no_case_exception_raise(
        self,
        user: Person,
        service: services.WordPresentationService,
        translations_meta: tuple[
            list[models.LangCategory],
            list[models_core.Source],
            list[models.LangMark],
            list[models_core.Period],
        ],
        conditions: types.CaseParameters,
    ) -> None:
        """Test that raises exception when no case for conditions."""
        categories, _, _, _ = translations_meta

        # Arrange
        category = categories[0]
        conditions['category'] = types.IdName(id=category.pk, name='')

        # Act & Assert
        with pytest.raises(exceptions.NoTranslationsAvailableException):
            service.get_case(user, conditions)
