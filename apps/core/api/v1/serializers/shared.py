"""Shared serializers."""

from rest_framework import serializers

from apps.lang import types


class IdNameSerializer(serializers.Serializer[types.IdName]):
    """Serializer for objects with id and name fields."""

    id = serializers.IntegerField()
    name = serializers.CharField()


# TODO: Rename 'label' field
# Use serializers.CharField(source='label')?
class ValueLabelSerializer(serializers.Serializer[types.ValueLabel]):
    """Serializer for objects with value and label fields."""

    value = serializers.CharField()
    label = serializers.CharField()  # type: ignore[assignment]
