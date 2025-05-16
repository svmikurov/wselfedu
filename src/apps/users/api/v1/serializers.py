"""Defines User serializer."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model (create/read operations)."""

    class Meta:
        """Metadata controlling serializer behavior."""

        model = User
        fields = [
            'username',
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'style': {'input_type': 'password'},
            },
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for user update operations."""

    class Meta:
        """Update-specific metadata."""

        model = User
        fields = [
            'username',
        ]
