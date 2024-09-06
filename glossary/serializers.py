"""Glossary serializer."""

from rest_framework import serializers

from glossary.models import Glossary


class GlossarySerializer(serializers.ModelSerializer):
    """Glossary serializer."""

    class Meta:
        """Construct the serializer."""

        model = Glossary
        fields = '__all__'
