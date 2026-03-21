"""Request parameters query null parser."""

from .abstract import AbstractRequestParamsQueryParser


class NullParser(
    AbstractRequestParamsQueryParser[dict[str, str], dict[str, str]]
):
    """Request parameters query null parser."""

    def parse(self, query: dict[str, str]) -> dict[str, str]:
        """Return query data."""
        return query
