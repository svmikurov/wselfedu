"""Defines serializers for Users application."""

from django.contrib.auth.models import Group, User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer[User]):
    """User serializer."""

    class Meta:
        """Metadata controlling serializer behavior."""

        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer[Group]):
    """Group serializer."""

    class Meta:
        """Metadata controlling serializer behavior."""

        model = Group
        fields = ['url', 'name']
