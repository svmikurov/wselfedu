"""Language discipline API & WEB response adapters."""

__all__ = [
    'WebPresentationAdapter',
    'ApiPresentationAdapter',
]

from .api_presentation import ApiPresentationAdapter
from .web_presentation import WebPresentationAdapter
