"""Word normalize tests."""

import pytest

from apps.lang.repos.translation import normalize_word


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
    assert normalize_word(text) == expected_text
