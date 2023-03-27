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
# from module_conduit import cookies_accept, sign_up
from data_conduit import user_data, user


class TestConduit(object):
    test_counter = 1

    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(service=service, options=options)

        URL = 'http://localhost:1667/#/'
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        self.browser.quit()

    def test_cookies_accept(self):
        self.cookie_policy_panel = self.browser.find_element(By.ID, 'cookie-policy-panel')
        self.btn_cookies_accept = self.browser.find_element(By.XPATH, '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        self.btn_cookies_accept.click()
        assert not self.btn_cookies_accept.is_displayed()
        # assert not self.cookie_policy_panel.is_enabled()

    def test_sign_up(self):
        # cookies_accept()

        self.btn_menu_sign_up = self.browser.find_element(By.XPATH, '//a[@href="#/register"]')
        self.btn_menu_sign_up.click()
        self.input_username = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        self.input_username.send_keys(user_data['username'] + str(self.test_counter))
        user.append(user_data['username'] + str(self.test_counter))
        self.input_email = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        self.input_email.send_keys(user_data['username'] + str(self.test_counter) + user_data['email'])
        self.input_password = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
        self.input_password.send_keys(user_data['password'])
        self.btn_func_sign_up = self.browser.find_element(By.XPATH,
                                                          '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        # self.btn_func_sign_up.click()
        assert self.btn_func_sign_up.is_displayed()
        assert self.input_username != ""
        assert self.input_email != ""
        assert self.input_password != ''

        time.sleep(2)
        self.test_counter += 1
        print()
        print(self.test_counter)
        print(user)
