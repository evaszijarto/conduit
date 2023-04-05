from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime, date, time, timezone

import time
from data_conduit import sign_up_user, login_user

# service = Service(executable_path=ChromeDriverManager().install())
# options = Options()
# options.add_experimental_option("detach", True)
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# browser = webdriver.Chrome(service=service, options=options)
#
# URL = 'http://localhost:1667/#/'
# browser.get(URL)
# browser.maximize_window()


def independent_cookies_accept(browser):
    btn_cookies_accept = browser.find_element(By.XPATH, '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
    btn_cookies_accept.click()

def independent_login():
    btn_menu_login = browser.find_element(By.XPATH, '//a[@href="#/login"]')
    btn_menu_login.click()
    input_email = browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
    input_email.send_keys(login_user['username'] + login_user['email'])
    input_password = browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
    input_password.send_keys(login_user['password'])
    btn_func_login = browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')

    btn_func_login.click()
    time.sleep(5)

