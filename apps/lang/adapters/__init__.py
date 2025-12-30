"""Language discipline API & WEB response adapters."""

__all__ = [
    'WebPresentationAdapter',
    'ApiPresentationAdapter',
    'WebTestAdapter',
]

from .api_presentation import ApiPresentationAdapter
from .test import WebTestAdapter
from .web_presentation import WebPresentationAdapter
