"""Language discipline services."""

__all__ = [
    'UpdateWordProgressService',
    'WordPresentationService',
]


from .presentation import WordPresentationService
from .progress import UpdateWordProgressService
