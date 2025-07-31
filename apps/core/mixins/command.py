"""Defines custom base command for management."""

from django.core.management.base import OutputWrapper
from django.core.management.color import Style


class DjStyledMessageMixin:
    """Mixin for out/err messages with Django style."""

    stdout: OutputWrapper
    stderr: OutputWrapper
    style: Style

    # Command message output

    def _msg_success(self, msg: str) -> None:
        self.stdout.write(self.style.SUCCESS(msg))

    def _msg_notice(self, msg: str) -> None:
        self.stderr.write(self.style.NOTICE(msg))

    def _msg_error(self, msg: str) -> None:
        self.stderr.write(self.style.ERROR(msg))

    def _msg_warning(self, msg: str) -> None:
        self.stdout.write(self.style.WARNING(msg))
