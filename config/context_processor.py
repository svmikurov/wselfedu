"""Context processor."""

import os

from django.http import HttpRequest


def pass_var_to_template(request: HttpRequest) -> dict[str, str | bool]:
    """Pass variables to the template.

    ENVIRONMENT_VARIABLES:
        -- IS_TEST
            Let start pytest without load bootstrap at templates.
            Load bootstrap makes tests unstable.

    Returns
    -------
    result : `dict`

    """
    return {
        'IS_TEST': os.getenv('IS_TEST'),
    }
