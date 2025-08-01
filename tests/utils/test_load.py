"""Test of load methods."""

import pytest

from utils.load import get_db_user, validate_username


class TestValidateUsername:
    """Test the validate username method."""

    def test_validate_username(self) -> None:
        """Test validate failed."""
        with pytest.raises(ValueError):
            validate_username('1')


class TestGetDBUser:
    """Test get DB user."""

    def test_valid_name(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test valid username."""
        monkeypatch.setenv('DB_USER', 'valid_user')
        assert get_db_user() == 'valid_user'

    def test_case_user_not_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test case then user is not defined."""
        monkeypatch.delenv('DB_USER')
        with pytest.raises(ValueError):
            assert get_db_user()
