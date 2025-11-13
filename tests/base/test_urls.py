"""Base class for url tests."""

from typing import Literal, Type, TypedDict

from django.urls import resolve
from rest_framework.viewsets import ViewSet


class UrlConfigType(TypedDict, total=True):
    """Path config typed dict."""

    path: str
    view_class: Type[ViewSet]
    action: dict[
        Literal['post', 'get'],
        str,
    ]


class BaseTestUrls:
    """Base url test.

    Example:
    -------
        class TestUrls(BaseTestUrls):
            URL_CONFIGS = {
                'study-params': {
                    'path': '/api/v1/lang/study/params/',
                    'view_class': WordStudyViewSet,
                    'action': {'get': 'params'},
                },
                'study-presentation': {
                    'path': '/api/v1/lang/study/presentation/',
                    'view_class': WordStudyViewSet,
                    'action': {'post': 'presentation'},
                },
            }

    """

    URL_CONFIGS: dict[str, UrlConfigType]

    def test_paths(self) -> None:
        """Test Word study paths."""
        for url_name, config in self.URL_CONFIGS.items():
            match = resolve(config['path'])

            assert match.url_name == url_name
            assert match.func.cls == config['view_class']  # type: ignore[attr-defined]

            # Check only the specified methods, ignoring the rest
            for method, action_name in config['action'].items():
                assert match.func.actions.get(method) == action_name  # type: ignore[attr-defined]
