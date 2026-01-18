"""Django settings for wselfedu project test mode."""

from .settings import *  # noqa: F403

# Exclude django toolbar panels for test mode
DEBUG_TOOLBAR_PANELS = []
