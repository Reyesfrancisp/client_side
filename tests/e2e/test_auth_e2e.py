import pytest
from playwright.sync_api import Page, expect

# Generate a unique username/email for testing to avoid conflicts
import uuid
unique_id = str(uuid.uuid4())[:8]

@pytest.mark.e2e
def test_positive_registration(page: Page, fastapi_server: str):
    """Positive: Register with valid data and confirm success message."""
    page.goto(f"{fastapi_server}register")
    
    page.fill("#username", f"testuser_{unique_id}")
    page.fill("#email", f"test_{unique_id}@example.com")
    page.fill("#first_name", "Test")
    page.fill("#last_name", "User")
    page.fill("#password", "SecurePass123!")
    page.fill("#confirm_password", "SecurePass123!")
    
    page.click("button[type='submit']")
    
    # Wait for the success message to appear
    success_msg = page.locator("#successMessage")
    expect(success_msg).to_be_visible(timeout=5000)
    expect(success_msg).to_contain_text("Registration successful")

@pytest.mark.e2e
def test_negative_registration_short_password(page: Page, fastapi_server: str):
    """Negative: Register with short password -> front-end error."""
    page.goto(f"{fastapi_server}register")
    
    page.fill("#username", f"badpass_{unique_id}")
    page.fill("#email", f"badpass_{unique_id}@example.com")
    page.fill("#first_name", "Test")
    page.fill("#last_name", "User")
    # Intentional short password that fails client validation
    page.fill("#password", "short") 
    page.fill("#confirm_password", "short")
    
    page.click("button[type='submit']")
    
    # Wait for the error message
    error_msg = page.locator("#errorMessage")
    expect(error_msg).to_be_visible(timeout=5000)
    expect(error_msg).to_contain_text("Password must be at least 8 characters long")

@pytest.mark.e2e
def test_positive_login(page: Page, fastapi_server: str):
    """Positive: Login with correct credentials, confirm success."""
    page.goto(f"{fastapi_server}login")
    
    # Using the credentials registered in the first test
    page.fill("#username", f"testuser_{unique_id}")
    page.fill("#password", "SecurePass123!")
    
    page.click("button[type='submit']")
    
    # On success, the UI redirects to /dashboard. Let's verify the URL changes.
    page.wait_for_url(f"{fastapi_server}dashboard", timeout=5000)
    expect(page).to_have_url(f"{fastapi_server}dashboard")

@pytest.mark.e2e
def test_negative_login_wrong_password(page: Page, fastapi_server: str):
    """Negative: Login with wrong password -> UI shows invalid credentials message."""
    page.goto(f"{fastapi_server}login")
    
    page.fill("#username", f"testuser_{unique_id}")
    page.fill("#password", "WrongPassword999!")
    
    page.click("button[type='submit']")
    
    # Wait for the error message
    error_msg = page.locator("#errorMessage")
    expect(error_msg).to_be_visible(timeout=5000)
    expect(error_msg).to_contain_text("Invalid username or password")