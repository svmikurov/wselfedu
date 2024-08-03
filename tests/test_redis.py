"""Test redis module."""

from django.core.cache import cache
from django.test import TestCase


class TestRedis(TestCase):
    """Test Redis cache."""

    def setUp(self):
        """Add cache to Redis."""
        cache.set('my_key', 'hello, world!', 30)

    def test_get_cache(self):
        """Get cache from Redis."""
        assert cache.get('my_key') == 'hello, world!'
