"""Language application DI container."""

from dependency_injector import containers, providers
from dependency_injector.providers import Factory

from .orchestrators import (
    CreateEnglishTranslation,
)
from .orchestrators.study import WordStudyOrchestrator
from .presenters import (
    EnglishTranslationPresenter,
    WordStudyParamsPresenter,
    WordStudyPresenter,
)
from .presenters.abc import WordStudyParamsPresenterABC
from .services.study import WordStudyService


class LanguageContainer(containers.DeclarativeContainer):
    """Language discipline DI container."""

    # CRUD
    # ----

    translation_orchestrator = providers.Factory(
        CreateEnglishTranslation,
    )
    translation_presenter = providers.Factory(
        EnglishTranslationPresenter,
    )

    # Word study
    # ----------

    db_service = providers.Factory(
        WordStudyOrchestrator,
    )
    task_service = providers.Factory(
        WordStudyService,
    )
    word_study_presenter = providers.Factory(
        WordStudyPresenter,
        db_service=db_service,
        task_service=task_service,
    )
    params_presenter: Factory[WordStudyParamsPresenterABC] = Factory(
        WordStudyParamsPresenter,
    )
