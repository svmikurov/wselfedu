"""Exercise conditions repository."""

from django.db.models import Manager, Model

from apps.lang.models import ExerciseConditions, TranslationConfiguration
from apps.users.models.user import Person
from contracts.entity.general import NullProtocol
from contracts.schemas.domain.exercise.params import (
    ExerciseParametersDTO,
    ExerciseSettingsDTO,
    LookupConditionsDTO,
)
from interfaces.protocols.domain.exercise import ExerciseParametersProtocol
from ports.abstract.repository import AbstractUserFetchRepository


# FIXME: Update NullProtocol to Generic type
class RegularParametersRepository(
    AbstractUserFetchRepository[
        NullProtocol,
        ExerciseParametersProtocol,
    ],
):
    """Regular condition repository."""

    def __init__(
        self,
        parameters_manager: Manager[ExerciseConditions],
        conf_manager: Manager[TranslationConfiguration],
    ) -> None:
        """Construct the repository."""
        self._parameters = parameters_manager
        self._conf = conf_manager

    def fetch(
        self,
        user: Person,
        filter: NullProtocol,
    ) -> ExerciseParametersProtocol:
        """Fetch user regular exercise settings."""
        parameters = self._get_parameters(user)
        conf = self._get_conf(user)
        return self._build_dto(parameters, conf)

    def _get_parameters(
        self,
        user: Person,
    ) -> ExerciseConditions | None:
        """Get translations query user conditions."""
        return self._parameters.filter(user=user).first()

    def _get_conf(self, user: Person) -> TranslationConfiguration | None:
        """Get exercise user configuration."""
        return self._conf.filter(user=user).first()

    def _build_dto(
        self,
        parameters: ExerciseConditions | None,
        conf: TranslationConfiguration | None,
    ) -> ExerciseParametersProtocol:
        return ExerciseParametersDTO(
            # ----------------------------
            # Translation query conditions
            # ----------------------------
            conditions=LookupConditionsDTO(
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
            else LookupConditionsDTO(),
            # -----------------------------
            # Translation exercise settings
            # -----------------------------
            settings=ExerciseSettingsDTO(
                display_order=conf.display_order,  # type: ignore
                item_count=conf.word_count,
            )
            if conf
            else ExerciseSettingsDTO(),
        )

    # TODO: Fix type ignore
    @staticmethod
    def _get_pk(instance: Model) -> str:
        return str(instance.pk) if instance else None  # type: ignore[return-value]
