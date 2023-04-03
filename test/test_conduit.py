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
import allure

import time
from data_conduit import sign_up_user, login_user, btns_menu_expected_text


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

    @allure.id('TC1')
    @allure.title('Oldal megnyitása')
    def test_open(self):
        page_name = self.browser.find_element(By.XPATH, '//a[@class="navbar-brand router-link-exact-active router-link-active"]')
        logo_name = self.browser.find_element(By.XPATH, '//h1[@class="logo-font"]')
        assert page_name.is_displayed()
        assert logo_name.is_displayed()
        assert page_name.text == "conduit"
        assert logo_name.text == "conduit"

    @allure.id('TC2')
    @allure.title('Adatkezelési nyilatkozat elfogadása')
    def test_cookies_accept(self):
        cookie_policy_panel = self.browser.find_element(By.ID, 'cookie-policy-panel')
        btn_cookies_accept = self.browser.find_element(By.XPATH, '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        assert cookie_policy_panel.is_enabled()
        assert btn_cookies_accept.is_enabled()
        btn_cookies_accept.click()
        # time.sleep(2)
        # assert cookie_policy_panel.get_attribute("value") == ""
        # assert btn_cookies_accept.get_attribute('value') == ''


    @allure.id('TC3')
    @allure.title('Regisztráció - Helyes adatokkal')
    def test_sign_up(self):
        self.test_cookies_accept()

        btn_menu_sign_up = self.browser.find_element(By.XPATH, '//a[@href="#/register"]')
        btn_menu_sign_up.click()
        input_username = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        input_username.send_keys(sign_up_user['username'])
        input_email = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        input_email.send_keys(sign_up_user['username'] + sign_up_user['email'])
        input_password = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
        input_password.send_keys(sign_up_user['password'])
        btn_func_sign_up = self.browser.find_element(By.XPATH,
                                                          '//button[@class="btn btn-lg btn-primary pull-xs-right"]')

        assert btn_func_sign_up.is_displayed()
        assert input_username != ""
        assert input_email != ""
        assert input_password != ''
        assert input_username.get_attribute('value') == sign_up_user['username']
        assert input_email.get_attribute('value') == sign_up_user['username'] + sign_up_user['email']
        assert input_password.get_attribute('value') == sign_up_user['password']

        btn_func_sign_up.click()
        time.sleep(3)
        message_ok = self.browser.find_element(By.XPATH, '//div[@class="swal-text"]')
        # message_ok = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="swal-text"]')))
        assert message_ok.text == 'Your registration was successful!'
        # print(message_ok.text)
        btn_ok_sign_up = self.browser.find_element(By.XPATH, '//button[@class="swal-button swal-button--confirm"]')
        assert btn_ok_sign_up.is_enabled()
        btn_ok_sign_up.click()

        self.test_open

    @allure.id('TC4')
    @allure.title('Bejelentkezés - Helyes adatokkal')
    def test_login(self):
        self.test_cookies_accept()

        btn_menu_login = self.browser.find_element(By.XPATH, '//a[@href="#/login"]')
        btn_menu_login.click()
        input_email = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        input_email.send_keys(login_user['username'] + login_user['email'])
        input_password = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
        input_password.send_keys(login_user['password'])
        btn_func_login = self.browser.find_element(By.XPATH,
                                                     '//button[@class="btn btn-lg btn-primary pull-xs-right"]')

        assert btn_func_login.is_displayed()
        assert input_email != ""
        assert input_password != ''
        assert input_email.get_attribute('value') == login_user['username'] + login_user['email']
        assert input_password.get_attribute('value') == login_user['password']

        btn_func_login.click()
        time.sleep(10)
        btn_menu_logged_in_user = self.browser.find_element(By.XPATH, '//a[@href="#/@conduit_test_user_10/"]')
        # btn_menu_logged_in_user = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/@conduit_test_user_10/"]')))
        assert btn_menu_logged_in_user.is_displayed()
        assert btn_menu_logged_in_user.is_enabled()
        assert btn_menu_logged_in_user.text == login_user['username']
        btns_menu_new = self.browser.find_elements(By.XPATH, '//a[@class="nav-link"]')
        n = 0
        for btn in btns_menu_new:
            # print(btn.text)
            assert btn.text == btns_menu_expected_text[n]
            n += 1
        self.test_open



