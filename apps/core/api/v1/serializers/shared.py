"""Shared serializers."""

from rest_framework import serializers

from ports.interfaces.request_data.api.general import CodeName, IdName


class IdNameSerializer(serializers.Serializer[IdName]):
    """Serializer for objects with id and name fields."""

    id = serializers.IntegerField()
    name = serializers.CharField()


class CodeNameSerializer(serializers.Serializer[CodeName]):
    """Serializer for objects with code and name fields."""

    code = serializers.CharField()
    name = serializers.CharField()
