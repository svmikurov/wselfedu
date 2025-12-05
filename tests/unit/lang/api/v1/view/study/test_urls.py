"""Test Word study paths."""

from apps.lang.api.v1.views.study import WordStudyViewSet
from tests.unit.base.test_urls import BaseApiUrlTest


class TestUrls(BaseApiUrlTest):
    """Test Word study ViewSet urls."""

    URL_CONFIGS = {
        'study-parameters': {
            'path': '/api/v1/lang/study/parameters/',
            'view_class': WordStudyViewSet,
            'action': {'get': 'parameters'},
        },
        'study-update-parameters': {
            'path': '/api/v1/lang/study/parameters/update/',
            'view_class': WordStudyViewSet,
            'action': {'put': 'update_parameters'},
        },
        'study-presentation': {
            'path': '/api/v1/lang/study/presentation/',
            'view_class': WordStudyViewSet,
            'action': {'post': 'presentation'},
        },
        'study-progress': {
            'path': '/api/v1/lang/study/progress/',
            'view_class': WordStudyViewSet,
            'action': {'post': 'progress'},
        },
    }
