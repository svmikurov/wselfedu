"""Language discipline api view DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Factory


class ApiViewContainer(DeclarativeContainer):
    """Language discipline api view DI container."""

    # =============================================
    # External dependencies
    # ---------------------------------------------
    handlers = DependenciesContainer()

    api_regular_presentation = Factory()
    study_parameters_repository = Factory()
    regular_translation_progress = Factory()
