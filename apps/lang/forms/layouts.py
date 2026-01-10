"""Django crispy layout components."""

from crispy_forms.layout import (  # type: ignore[import-untyped]
    Button,
    Div,
    Submit,
)
from django.utils.translation import gettext as _


def create_cancel_button(target_id: str) -> Button:
    """Create crispy "cancel" button."""
    return Button(
        'cancel',
        _('button.cancel'),
        css_class='wse-btn',
        onclick=f'document.getElementById({target_id!r}).remove()',
    )


def create_submit_button() -> Submit:
    """Create crispy "submit" button."""
    return Submit(
        'submit',
        _('button.submit'),
        css_class='wse-btn',
    )


def create_button_row(target_id: str) -> Div:
    """Crete crispy button row."""
    return Div(
        create_cancel_button(target_id),
        create_submit_button(),
        css_class='d-flex gap-2 justify-content-end',
    )
