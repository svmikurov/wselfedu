"""Translation presentation adapter for WEB context."""

import json

from django.urls import reverse

from apps.lang import types

from . import base


class TranslationAdapterWEB(base.BaseTranslationAdapterWEB):
    """Translation study presentation adapter for WEB context."""

    def to_context(self, data: types.TranslationCase) -> types.TranslationWEB:
        """Adapt the presentation case of translation for WEB."""
        increment_progress: types.UpdateProgressT = {
            'case_uuid': str(data['case_uuid']),
            'is_known': 'true',
        }
        decrement_progress: types.UpdateProgressT = {
            'case_uuid': str(data['case_uuid']),
            'is_known': 'false',
        }
        return {
            'case_uuid': str(data['case_uuid']),
            'definition': data['definition'],
            'explanation': data['explanation'],
            'progress': {
                'current': str(data['info']['progress'] or '0'),
                'update_url': reverse('lang_api:study-progress'),
                'increment_payload': json.dumps(increment_progress),
                'decrement_payload': json.dumps(decrement_progress),
            },
        }
