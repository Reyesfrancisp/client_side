import pytest
from playwright.sync_api import Page, expect
import uuid

@pytest.mark.e2e
def test_positive_registration(page: Page, fastapi_server: str):
    """Positive: Register with valid data and confirm success message."""
    # Generate unique ID inside the test so it is fresh every time
    unique_id = str(uuid.uuid4())[:8]
    
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
    unique_id = str(uuid.uuid4())[:8]
    
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
    unique_id = str(uuid.uuid4())[:8]
    username = f"loginuser_{unique_id}"
    password = "SecurePass123!"
    
    # 1. Register the user first so we guarantee the user exists for the login test
    page.goto(f"{fastapi_server}register")
    page.fill("#username", username)
    page.fill("#email", f"login_{unique_id}@example.com")
    page.fill("#first_name", "Login")
    page.fill("#last_name", "User")
    page.fill("#password", password)
    page.fill("#confirm_password", password)
    page.click("button[type='submit']")
    
    # Wait for the UI's 2-second JS redirect to the login page
    page.wait_for_url(f"{fastapi_server}login", timeout=5000)
    
    # 2. Perform the Login test
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("button[type='submit']")
    
    # On success, the UI redirects to /dashboard. Let's verify the URL changes.
    page.wait_for_url(f"{fastapi_server}dashboard", timeout=5000)
    expect(page).to_have_url(f"{fastapi_server}dashboard")

@pytest.mark.e2e
def test_negative_login_wrong_password(page: Page, fastapi_server: str):
    """Negative: Login with wrong password -> UI shows invalid credentials message."""
    unique_id = str(uuid.uuid4())[:8]
    username = f"loginuser_{unique_id}"
    password = "SecurePass123!"
    
    # 1. Register the user first 
    page.goto(f"{fastapi_server}register")
    page.fill("#username", username)
    page.fill("#email", f"wrongpass_{unique_id}@example.com")
    page.fill("#first_name", "Wrong")
    page.fill("#last_name", "Pass")
    page.fill("#password", password)
    page.fill("#confirm_password", password)
    page.click("button[type='submit']")
    
    # Wait for the UI redirect to the login page
    page.wait_for_url(f"{fastapi_server}login", timeout=5000)
    
    # 2. Attempt login with WRONG password
    page.fill("#username", username)
    page.fill("#password", "WrongPassword999!")
    page.click("button[type='submit']")
    
    # Wait for the error message
    error_msg = page.locator("#errorMessage")
    expect(error_msg).to_be_visible(timeout=5000)
    expect(error_msg).to_contain_text("Invalid username or password")