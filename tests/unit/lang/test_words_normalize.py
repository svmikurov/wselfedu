"""Word normalize tests."""

import pytest

from apps.lang.repositories.translation import _normalize_word


@pytest.mark.parametrize(
    'text, expected_text',
    [
        ('', ''),
        (' text ', 'text'),
        (', text -, ', 'text'),
        ('#text,!.?', 'text'),
        ('text, text', 'text, text'),
    ],
)
def test_word_normalize(
    text: str,
    expected_text: str,
) -> None:
    """Test correct text normalize."""
    assert _normalize_word(text) == expected_text
