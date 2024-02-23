"""
The module contains functions for briefly presenting tests.
"""
from playwright.sync_api import Page, expect


def is_role_visible(page: Page, role: str, name: str):
    """Test if there is an element on the page with a certain text."""
    expect(page.get_by_role(role=role, name=name)).to_be_visible()
