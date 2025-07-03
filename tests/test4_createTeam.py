import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_superuser_can_create(browser):
    browser.get('http://localhost:8000/')

    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Login'))
    ).click()

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )
    browser.find_element(By.NAME, 'username').send_keys('Finn')
    browser.find_element(By.NAME, 'password').send_keys('Maverick')
    browser.find_element(By.XPATH, '//button[@type="submit"]').click()

    time.sleep(5)

    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Teams'))
    ).click()

    time.sleep(5)

    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Create Team'))
    ).click()

    time.sleep(5)

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, 'name'))
    )
    new_team_name = f"Selenium Team {int(time.time())}"
    browser.find_element(By.NAME, 'name').send_keys(new_team_name)
    browser.find_element(By.XPATH, '//button[@type="submit"]').click()

    time.sleep(5)

    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Teams'))
    ).click()

    time.sleep(5)

    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), new_team_name)
    )

    time.sleep(5)