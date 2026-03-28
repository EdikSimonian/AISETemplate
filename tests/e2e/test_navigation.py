"""
Navigation sidebar tests.

Tests run against the logged-out state (no credentials needed).
To test the logged-in state, set TEST_EMAIL and TEST_PASSWORD env vars.
"""

import os

import pytest
from playwright.sync_api import Page, expect


class TestLoggedOutNavigation:
    def test_sidebar_shows_login_link(self, page: Page):
        """Sidebar should show 'Log in' when not authenticated."""
        expect(page.get_by_role("link", name="Log in")).to_be_visible()

    def test_sidebar_shows_signup_link(self, page: Page):
        """Sidebar should show 'Sign up' when not authenticated."""
        expect(page.get_by_role("link", name="Sign up")).to_be_visible()

    def test_sidebar_does_not_show_home(self, page: Page):
        """Home link should not appear when logged out."""
        expect(page.get_by_role("link", name="Home")).not_to_be_visible()

    def test_sidebar_does_not_show_logout(self, page: Page):
        """Log out button should not appear when logged out."""
        expect(page.get_by_role("button", name="Log out")).not_to_be_visible()


class TestLoginPage:
    def test_login_form_has_email_field(self, page: Page):
        page.get_by_role("link", name="Log in").click()
        page.wait_for_selector("[data-testid='stForm']")
        expect(page.get_by_label("Email")).to_be_visible()

    def test_login_form_has_password_field(self, page: Page):
        page.get_by_role("link", name="Log in").click()
        page.wait_for_selector("[data-testid='stForm']")
        expect(page.get_by_label("Password")).to_be_visible()

    def test_login_shows_error_on_empty_submit(self, page: Page):
        page.get_by_role("link", name="Log in").click()
        page.wait_for_selector("[data-testid='stForm']")
        page.get_by_role("button", name="Log in").click()
        expect(page.get_by_text("Email and password are required.")).to_be_visible()

    def test_login_page_has_signup_link(self, page: Page):
        page.get_by_role("link", name="Log in").click()
        page.wait_for_selector("[data-testid='stForm']")
        expect(page.get_by_role("button", name="Sign up")).to_be_visible()


class TestSignupPage:
    def test_signup_form_has_required_fields(self, page: Page):
        page.get_by_role("link", name="Sign up").click()
        page.wait_for_selector("[data-testid='stForm']")
        expect(page.get_by_label("Full name")).to_be_visible()
        expect(page.get_by_label("Email")).to_be_visible()
        expect(page.get_by_label("Password")).to_be_visible()

    def test_signup_shows_error_on_empty_submit(self, page: Page):
        page.get_by_role("link", name="Sign up").click()
        page.wait_for_selector("[data-testid='stForm']")
        page.get_by_role("button", name="Create account").click()
        expect(page.get_by_text("All fields are required.")).to_be_visible()

    def test_signup_shows_error_on_short_password(self, page: Page):
        page.get_by_role("link", name="Sign up").click()
        page.wait_for_selector("[data-testid='stForm']")
        page.get_by_label("Full name").fill("Test User")
        page.get_by_label("Email").fill("test@example.com")
        page.get_by_label("Password").fill("abc")
        page.get_by_role("button", name="Create account").click()
        expect(page.get_by_text("Password must be at least 6 characters.")).to_be_visible()


@pytest.mark.skipif(
    not os.environ.get("TEST_EMAIL"),
    reason="TEST_EMAIL not set — skipping logged-in navigation tests",
)
class TestLoggedInNavigation:
    def _login(self, frame, email, password):
        frame.locator("a", has_text="Log in").click()
        frame.get_by_role("textbox", name="Email").fill(email)
        frame.get_by_role("textbox", name="Password").fill(password)
        frame.get_by_role("button", name="Log in").click()
        frame.locator("text=Workshop App").wait_for(timeout=15000)

    def _get_frame(self, page):
        for f in page.frames:
            if f.url.endswith("/~/+/"):
                return f
        return page.frames[-1]

    def test_sidebar_shows_home_after_login(self, page: Page):
        """After login, sidebar shows Home nav link."""
        frame = self._get_frame(page)
        self._login(frame, os.environ["TEST_EMAIL"], os.environ["TEST_PASSWORD"])
        assert "Home" in frame.evaluate("document.body.innerText")

    def test_sidebar_shows_settings_after_login(self, page: Page):
        """After login, sidebar shows Settings nav link."""
        frame = self._get_frame(page)
        self._login(frame, os.environ["TEST_EMAIL"], os.environ["TEST_PASSWORD"])
        assert "Settings" in frame.evaluate("document.body.innerText")

    def test_sidebar_shows_logout_after_login(self, page: Page):
        """After login, Log out button appears in sidebar."""
        frame = self._get_frame(page)
        self._login(frame, os.environ["TEST_EMAIL"], os.environ["TEST_PASSWORD"])
        assert "Log out" in frame.evaluate("document.body.innerText")

    def test_logout_returns_to_login_view(self, page: Page):
        """Clicking Log out shows login nav again."""
        frame = self._get_frame(page)
        self._login(frame, os.environ["TEST_EMAIL"], os.environ["TEST_PASSWORD"])
        frame.get_by_role("button", name="Log out").click()
        frame.locator("text=Log in").first.wait_for(timeout=10000)
        assert "Log in" in frame.evaluate("document.body.innerText")
