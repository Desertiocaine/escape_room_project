import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_invalid_user_cannot_access_room(browser):
    browser.get('http://localhost:8000/')
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Rooms'))).click()
    room_links = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul li a'))
    )
    print(f"Found {len(room_links)} room links")
    assert len(room_links) >= 5, "Less than 5 rooms found"
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '(//ul/li/a)[5]'))
    ).click()
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
    browser.find_element(By.NAME, 'username').send_keys('invalid_user')
    browser.find_element(By.NAME, 'password').send_keys('wrong_password')
    browser.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(2)  # Pause to see the result
    assert "Please enter a correct username and password" in browser.page_source
