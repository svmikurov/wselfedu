"""Repository DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from .. import repositories


class RepositoryContainer(DeclarativeContainer):
    """Repository DI container."""

    # ----------------
    # English language
    # ----------------

    translation = Factory(repositories.TranslationRepository)
    rule = Factory(repositories.RuleRepository)

    # ------------------------------------
    # Regular exercise settings repository
    # ------------------------------------

    study_parameters = Factory(repositories.StudyParametersRepository)
    study_settings = Factory(repositories.StudySettingsRepository)
