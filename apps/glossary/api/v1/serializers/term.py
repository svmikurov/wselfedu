"""Term serializer."""

from rest_framework import serializers

from apps.glossary.models import Term


class TermSerializer(serializers.ModelSerializer[Term]):
    """Serializer for Term."""

    class Meta:
        """Serializer configuration."""

        model = Term
        fields = [
            'id',
            'name',
            'definition',
            'created_at',
        ]
