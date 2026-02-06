"""View-injected exercise dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer


class ViewExerciseContainer(DeclarativeContainer):
    """Container providing view-injected exercise dependencies.

    Views reference attributes from this container without
    modification, while dependency implementations can be
    changed in the container itself.
    """

    # Exercise services & repositories
    services = DependenciesContainer()
    repositories = DependenciesContainer()

    # Exercises
    presentation_handlers = DependenciesContainer()
    test_handlers = DependenciesContainer()

    # --------------
    # Study settings
    # --------------

    study_settings_repository = repositories.study_settings
    study_parameters_repository = repositories.study_parameters

    # ---------------------
    # Presentation exercise
    # ---------------------

    web_regular_presentation = presentation_handlers.web_regular

    api_regular_presentation = presentation_handlers.api_regular

    # -------------
    # Test exercise
    # -------------

    web_regular_test = test_handlers.web_regular
    web_detail_test = test_handlers.web_detail  # Refactoring

    # ----------------------------------
    # Regular translation study progress
    # ----------------------------------

    regular_translation_progress = services.regular_translation_progress
