"""Base class for api url tests."""

from typing import Literal, Type, TypedDict

from django.urls import resolve
from django.views import View
from rest_framework.viewsets import ViewSet

# =================================================
# DRF
# =================================================


class ApiUrlConfigType(TypedDict, total=True):
    """Path config typed dict."""

    path: str
    view_class: Type[ViewSet]
    action: dict[
        Literal['post', 'get', 'put'],
        str,
    ]


class BaseApiUrlTest:
    """Api url base test.

    Example
    -------
        class TestUrls(BaseApiUrlTest):
            URL_CONFIGS = {
                'study-params': {
                    'path': '/api/v1/lang/study/parameters/',
                    'view_class': WordStudyViewSet,
                    'action': {'get': 'parameters'},
                },
                'study-presentation': {
                    'path': '/api/v1/lang/study/presentation/',
                    'view_class': WordStudyViewSet,
                    'action': {'post': 'presentation'},
                },
            }

    """

    __test__ = False

    URL_CONFIGS: dict[str, ApiUrlConfigType]

    def test_paths(self) -> None:
        """Test Word study paths."""
        for url_name, config in self.URL_CONFIGS.items():
            match = resolve(config['path'])

            assert match.url_name == url_name
            assert match.func.cls == config['view_class']  # type: ignore[attr-defined]

            # Check only the specified methods, ignoring the rest
            for method, action_name in config['action'].items():
                assert match.func.actions.get(method) == action_name  # type: ignore[attr-defined]


# =================================================
# Pure Django
# =================================================


class UrlConfigType(TypedDict, total=True):
    """Path config typed dict."""

    path: str
    view_class: Type[View]
    name: str


class BaseUrlTest:
    """Base url test for pure Django.

    Example:
    -------
        class TestUrls(BaseUrlTest):
            URL_CONFIGS = {
                'home': {
                    'path': '/',
                    'view_class': HomeView,
                    'name': 'home',
                },
                'about': {
                    'path': '/about/',
                    'view_class': AboutView,
                    'name': 'about',
                },
                'user-profile': {
                    'path': '/user/profile/',
                    'view_class': UserProfileView,
                    'name': 'user-profile',
                },
            }

    """

    __test__ = False

    URL_CONFIGS: dict[str, UrlConfigType]

    def test_urls_resolve(self) -> None:
        """Test that URLs resolve to correct view classes."""
        for _config_name, config in self.URL_CONFIGS.items():
            match = resolve(config['path'])

            # Check URL name
            assert match.url_name == config['name']

            # For class-based views
            if hasattr(match.func, 'view_class'):
                assert match.func.view_class == config['view_class']
            else:
                # For function-based views
                assert match.func == config['view_class']
