"""Language app base serializers."""

from rest_framework import serializers

from apps.core.api.v1 import serializers as core
from apps.lang import types


class OptionsSerializer(serializers.Serializer[types.Options]):
    """Translation options serializer."""

    categories = core.IdNameSerializer(many=True)
    marks = core.IdNameSerializer(many=True)
    sources = core.IdNameSerializer(many=True)
    periods = core.IdNameSerializer(many=True)
    translation_orders = core.CodeNameSerializer(many=True)


class TranslationMetaSerializer(serializers.Serializer[types.WordParameters]):
    """Translation meta serializer."""

    category = core.IdNameSerializer(allow_null=True)
    mark = core.IdNameSerializer(allow_null=True)
    word_source = core.IdNameSerializer(allow_null=True)
    start_period = core.IdNameSerializer(allow_null=True)
    end_period = core.IdNameSerializer(allow_null=True)


class TranslationSettingsSerializer(
    serializers.Serializer[types.TranslationSettings]
):
    """Translation settings serializer."""

    translation_order = core.CodeNameSerializer(allow_null=True)
    word_count = serializers.IntegerField(allow_null=True)


class PresentationSettingsSerializer(
    serializers.Serializer[types.PresentationSettings]
):
    """Presentation settings serializer."""

    question_timeout = serializers.FloatField(allow_null=True)
    answer_timeout = serializers.FloatField(allow_null=True)
