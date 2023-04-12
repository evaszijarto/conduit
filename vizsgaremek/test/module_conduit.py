from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from datetime import time
import time
import csv
from data_conduit import sign_up_user


def independent_cookies_accept(browser):
    btn_cookies_accept = browser.find_element(By.XPATH,
                                              '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
    btn_cookies_accept.click()


def independent_login(browser):
    btn_menu_login = browser.find_element(By.XPATH, '//a[@href="#/login"]')
    btn_menu_login.click()
    input_email = browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
    input_email.send_keys(sign_up_user['username'] + sign_up_user['email'])
    input_password = browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
    input_password.send_keys(sign_up_user['password'])
    btn_func_login = browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')

    btn_func_login.click()
    time.sleep(2)


def logged_in_user_site_from_home(browser):
    btn_menu_logged_in_user = \
        WebDriverWait(browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[2]
    btn_menu_logged_in_user.click()
    time.sleep(2)
    browser.refresh()
    time.sleep(2)


def logged_in_user_site_from_article(browser):
    btn_menu_logged_in_user = \
        WebDriverWait(browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[3]
    btn_menu_logged_in_user.click()
    time.sleep(2)
    browser.refresh()
    time.sleep(2)


def create_more_articles_from_file(browser, file_path):
    with open(file_path, 'r', encoding='UTF-8') as datas:
        data_reader = csv.reader(datas, delimiter=';')
        for data in data_reader:
            btn_new_articel = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//a[@href="#/editor"]')))
            btn_new_articel.click()
            time.sleep(2)

            input_article_title = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//input[@class="form-control form-control-lg"]')))
            input_article_about = browser.find_element(By.XPATH, '//input[@class="form-control"]')
            input_article = browser.find_element(By.XPATH, '//textarea[@class="form-control"]')
            input_article_tag = browser.find_element(By.XPATH, '//input[@placeholder="Enter tags"]')

            input_article_title.send_keys(data[0])
            input_article_about.send_keys(data[1])
            input_article.send_keys(data[2])
            input_article_tag.send_keys(data[3])

            btn_publish = browser.find_element(By.XPATH, '//button[@type="submit"]')
            btn_publish.click()
            time.sleep(5)


def go_home(browser):
    btn_menu_home = \
        WebDriverWait(browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[0]
    btn_menu_home.click()


def list_upload(webelements_name, list_name):
    for article in webelements_name:
        list_name.append(article.text)
