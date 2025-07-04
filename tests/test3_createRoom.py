import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_valid_user_can_create_room(browser):
    browser.get('http://localhost:8000/')

    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Login'))).click()

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
    browser.find_element(By.NAME, 'username').send_keys('Kenneth')
    browser.find_element(By.NAME, 'password').send_keys('Euell2360!')
    browser.find_element(By.XPATH, '//button[@type="submit"]').click()

    time.sleep(5)

    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Rooms'))).click()

    time.sleep(5)

    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Create New Room'))).click()

    time.sleep(5)

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'name')))
    browser.find_element(By.NAME, 'name').send_keys(f'Test Room {int(time.time())}')
    element = browser.find_element(By.NAME, 'description')
    element.clear()
    browser.find_element(By.NAME, 'description').send_keys('Selenium test room.')
    element = browser.find_element(By.NAME, 'max_players')
    element.clear()
    browser.find_element(By.NAME, 'max_players').send_keys('5')

    time.sleep(5)

    browser.find_element(By.XPATH, '//button[@type="submit"]').click()

    time.sleep(5)

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    assert "Test Room" in browser.page_source

    time.sleep(5)
