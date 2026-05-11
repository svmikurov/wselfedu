"""Exercise WEB response."""

from typing import Any

from ports.contract.response.web import HtmlResponseProtocol

from ..domain.exercise import (
    PresentationDomainResultProtocol,
    TestDomainResultProtocol,
)

PresentationResponse = HtmlResponseProtocol[
    PresentationDomainResultProtocol,
    Any,
    Any,
]
"""Presentation exercise response.
"""

TestResponse = HtmlResponseProtocol[
    TestDomainResultProtocol,
    Any,
    Any,
]
"""Test exercise response.
"""
