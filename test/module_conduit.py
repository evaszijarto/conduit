from data_conduit import user_data, user

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

service = Service(executable_path=ChromeDriverManager().install())
options = Options()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(service=service, options=options)

URL = 'http://localhost:1667/#/'
# browser.get(URL)
# browser.maximize_window()
#
#
def cookies_accept():
    btn_cookies_accept = browser.find_element(By.XPATH, '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
    btn_cookies_accept.click()

#
# def sign_up(user_number):
#     btn_menu_sign_up = browser.find_element(By.XPATH, '//a[@href="#/register"]')
#     btn_menu_sign_up.click()
#     input_username = browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
#     # input_username.send_keys(user_data['username'] + str(user_number))
#     # user.append(user_data['username'] + str(user_number))
#     input_email = browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
#     # input_email.send_keys(user_data['username'] + str(user_number) + user_data['email'])
#     input_password = browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
#     # input_password.send_keys(user_data['password'])
#     btn_func_sign_up = browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
#     # btn_func_sign_up.click()
#
#
# # cookies_accept()
# # sign_up(1)
#
# # browser.quit()
