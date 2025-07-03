import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def browser():
    driver = webdriver.Chrome()  # Or use the appropriate driver for your browser
    yield driver
    driver.quit()

def test_valid_user_can_view_teams(browser):
    browser.get('http://localhost:8000/')
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Teams'))).click()
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
    browser.find_element(By.NAME, 'username').send_keys('Kenneth')
    browser.find_element(By.NAME, 'password').send_keys('Euell2360!')
    browser.find_element(By.XPATH, '//button[@type="submit"]').click()
    # Wait for teams page to load
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    time.sleep(2)  # Optional: to see the result
    assert "Team" in browser.page_source
