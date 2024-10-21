"""Cache tests."""

from django.core.cache import cache
from django.test import TestCase

from contrib.cache import get_cache_dict, set_cache_dict


class TestDjangoCache(TestCase):
    """Test Django cache."""

    def setUp(self) -> None:
        """Add data to Django cache."""
        cache.set('my_key', 'hello, world!', 30)

    def test_get_cache(self) -> None:
        """Get data from Django cache."""
        assert cache.get('my_key') == 'hello, world!'


class TestRedisCacheMapping(TestCase):
    """Test Redis cache mapping."""

    def setUp(self) -> None:
        """Add mapping to Redis cache."""
        mapping = {'one': 1, 'two': '2'}
        set_cache_dict('key', mapping)

    def test_cache_mapping(self) -> None:
        """Test get mapping from Redis cache."""
        mapping = get_cache_dict('key')
        assert mapping == {'one': '1', 'two': '2'}
