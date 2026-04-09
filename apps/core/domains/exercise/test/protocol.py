"""Protocol for test exercise interface."""

from typing import Protocol, TypeVar

from ..protocol import Candidate, HasOptions, HasOptionValue

OptionT = TypeVar('OptionT', bound=Candidate)


class TestDomainCreateResultProtocol(
    HasOptionValue,
    HasOptions[OptionT],
    Protocol,
):
    """Test exercise create domain result DTO interface."""
