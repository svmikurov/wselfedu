"""Exercise conditions repository."""

from django.db.models import Manager, Model

from apps.lang import models
from apps.lang.schemas import LookupCondition, SettingsModel
from apps.users.models.user import Person

from .abc import ByUserRepositoryABC
from .dto import RegularParameters


class RegularParametersRepository(ByUserRepositoryABC[RegularParameters]):
    """Regular condition repository."""

    def __init__(
        self,
        parameters_manager: Manager[models.Parameters],
        settings_manager: Manager[models.TranslationSetting],
    ) -> None:
        """Construct the repository."""
        self._parameters = parameters_manager
        self._settings = settings_manager

    def fetch(self, user: Person) -> RegularParameters:
        """Fetch user regular exercise settings."""
        parameters = self._get_parameters(user)
        settings = self._get_settings(user)
        return self._build_dto(parameters, settings)

    def _get_parameters(self, user: Person) -> models.Parameters | None:
        """Get translations query user conditions."""
        return self._parameters.filter(user=user).first()

    def _get_settings(self, user: Person) -> models.TranslationSetting | None:
        """Get exercise user settings."""
        return self._settings.filter(user=user).first()

    def _build_dto(
        self,
        parameters: models.Parameters | None,
        settings: models.TranslationSetting | None,
    ) -> RegularParameters:
        return RegularParameters(
            # ----------------------------
            # Translation query conditions
            # ----------------------------
            conditions=LookupCondition(
                category=self._get_pk(parameters.category),  # type: ignore
                source=self._get_pk(parameters.word_source),  # type: ignore
                mark=[parameters.mark.pk] if parameters.mark else [],
                start_period=self._get_pk(parameters.start_period),  # type: ignore
                end_period=self._get_pk(parameters.end_period),  # type: ignore
                is_study=parameters.is_study,  # type: ignore
                is_repeat=parameters.is_repeat,  # type: ignore
                is_examine=parameters.is_examine,  # type: ignore
                is_know=parameters.is_know,  # type: ignore
            )
            if parameters
            else None,
            # -----------------------------
            # Translation exercise settings
            # -----------------------------
            settings=SettingsModel(
                display_order=settings.display_order,  # type: ignore
                item_count=settings.word_count,
            )
            if settings
            else None,
        )

    # TODO: Fix type ignore
    @staticmethod
    def _get_pk(instance: Model) -> str:
        return str(instance.pk) if instance else None  # type: ignore[return-value]
