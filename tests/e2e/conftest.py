"""
Playwright e2e fixtures.

Usage:
    pip install -r requirements-dev.txt
    playwright install chromium
    pytest tests/e2e/ -v

The APP_URL env var controls which instance is tested (default: localhost:8501).
Set APP_URL to your Streamlit Cloud URL to test the deployed app.
"""

import os

import pytest

APP_URL = os.environ.get("APP_URL", "http://localhost:8501")


@pytest.fixture(scope="session")
def app_url() -> str:
    return APP_URL


@pytest.fixture
def page(page, app_url):
    """Navigate to the app before each test."""
    page.goto(app_url)
    # Wait for Streamlit to finish its initial render
    page.wait_for_selector("[data-testid='stApp']", timeout=15000)
    return page
