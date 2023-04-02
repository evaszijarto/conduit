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
# from module_conduit import cookies_accept
from data_conduit import user_data, user


class TestConduit(object):

    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(service=service, options=options)

        URL = 'http://localhost:1667/#/'
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        self.browser.quit()

    def test_cookies_accept(self):
        cookie_policy_panel = self.browser.find_element(By.ID, 'cookie-policy-panel')
        btn_cookies_accept = self.browser.find_element(By.XPATH, '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        assert cookie_policy_panel.is_enabled()
        assert btn_cookies_accept.is_enabled()
        btn_cookies_accept.click()
        # assert not btn_cookies_accept.is_displayed()

    def test_sign_up(self):
        # cookies_accept()

        btn_menu_sign_up = self.browser.find_element(By.XPATH, '//a[@href="#/register"]')
        btn_menu_sign_up.click()
        input_username = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        input_username.send_keys(user_data['username'])
        user.append(user_data['username'])
        input_email = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        input_email.send_keys(user_data['username'] + user_data['email'])
        input_password = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
        input_password.send_keys(user_data['password'])
        btn_func_sign_up = self.browser.find_element(By.XPATH,
                                                          '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        assert btn_func_sign_up.is_displayed()
        assert input_username != ""
        assert input_email != ""
        assert input_password != ''

        # self.btn_func_sign_up.click()
