import pytest
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
import csv

import time
from data_conduit import sign_up_user, btns_menu_logged_in_expected_text, btns_menu_logged_out_expected_text, \
    new_article_data, update_article_data
from tmodule_conduit import independent_cookies_accept, independent_login, logged_in_user_site_from_home, \
    list_of_datas_and_titles, logged_in_user_site_from_article, create_more_articles


class TestConduit(object):
    article_counter = 0

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
        # pass # pycharm futtatáshoz kell
        self.browser.quit()

    @allure.id('TC1')
    @allure.title('Oldal megnyitása')
    def test_open(self):
        page_name = self.browser.find_element(By.XPATH,
                                              '//a[@class="navbar-brand router-link-exact-active router-link-active"]')
        logo_name = self.browser.find_element(By.XPATH, '//h1[@class="logo-font"]')
        assert page_name.is_displayed()
        assert logo_name.is_displayed()
        assert page_name.text == "conduit"
        assert logo_name.text == "conduit"

    @allure.id('TC2')
    @allure.title('Adatkezelési nyilatkozat elfogadása')
    def test_cookies_accept(self):
        cookie_policy_panel = self.browser.find_element(By.ID, 'cookie-policy-panel')
        btn_cookies_accept = self.browser.find_element(By.XPATH,
                                                       '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        assert cookie_policy_panel.is_enabled()
        assert btn_cookies_accept.is_enabled()
        btn_cookies_accept.click()

        try:
            cookie_policy_panel = self.browser.find_element(By.ID, 'cookie-policy-panel')
        except Exception as e_info:
            assert True

    @allure.id('TC3')
    @allure.title('Regisztráció - Helyes adatokkal')
    def test_sign_up(self):
        independent_cookies_accept(self.browser)

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
        # message_ok = self.browser.find_element(By.XPATH, '//div[@class="swal-text"]')
        message_ok = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="swal-text"]')))
        assert message_ok.text == 'Your registration was successful!'
        # print(message_ok.text)
        btn_ok_sign_up = self.browser.find_element(By.XPATH, '//button[@class="swal-button swal-button--confirm"]')
        assert btn_ok_sign_up.is_enabled()
        btn_ok_sign_up.click()

    @allure.id('TC4')
    @allure.title('Bejelentkezés - Helyes adatokkal')
    def test_login(self):
        independent_cookies_accept(self.browser)

        btn_menu_login = self.browser.find_element(By.XPATH, '//a[@href="#/login"]')
        btn_menu_login.click()
        input_email = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        input_email.send_keys(sign_up_user['username'] + sign_up_user['email'])
        input_password = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
        input_password.send_keys(sign_up_user['password'])
        btn_func_login = self.browser.find_element(By.XPATH,
                                                   '//button[@class="btn btn-lg btn-primary pull-xs-right"]')

        assert btn_func_login.is_displayed()
        assert input_email != ""
        assert input_password != ''
        assert input_email.get_attribute('value') == sign_up_user['username'] + sign_up_user['email']
        assert input_password.get_attribute('value') == sign_up_user['password']

        btn_func_login.click()
        time.sleep(5)
        # btn_menu_logged_in_user = self.browser.find_element(By.XPATH, '//a[@href="#/@conduit_test_user_10/"]')
        # btn_menu_logged_in_user = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/@conduit_test_user_10/"]')))
        btn_menu_logged_in_user = \
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[
                2]
        # print(len(btn_menu_logged_in_user))
        assert btn_menu_logged_in_user.is_displayed()
        assert btn_menu_logged_in_user.is_enabled()
        assert btn_menu_logged_in_user.text == sign_up_user['username']
        btns_menu_new = self.browser.find_elements(By.XPATH, '//a[@class="nav-link"]')
        n = 0
        for btn in btns_menu_new:
            # print(btn.text)
            assert btn.text == btns_menu_logged_in_expected_text[n]
            n += 1

    @allure.id('TC5')
    @allure.title('Kijelentkezés - Helyes adatokkal')
    def test_log_out(self):
        independent_cookies_accept(self.browser)
        independent_login(self.browser)
        time.sleep(5)
        btn_menu_log_out = \
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[
                3]
        btn_menu_log_out.click()
        time.sleep(5)
        page_name = self.browser.find_element(By.XPATH,
                                              '//a[@class="navbar-brand router-link-exact-active router-link-active"]')
        logo_name = self.browser.find_element(By.XPATH, '//h1[@class="logo-font"]')
        assert page_name.is_displayed()
        assert logo_name.is_displayed()
        assert page_name.text == "conduit"
        assert logo_name.text == "conduit"

        btns_menu_logged_out = self.browser.find_elements(By.XPATH, '//li[@class="nav-item"]')
        n = 0
        for btn in btns_menu_logged_out:
            # print(btn.text)
            assert btn.text == btns_menu_logged_out_expected_text[n]
            n += 1

    @allure.id('TC6')
    @allure.title('Új adat bevitel - Helyes adatokkal')
    def test_data_creation(self):
        independent_cookies_accept(self.browser)
        independent_login(self.browser)
        time.sleep(5)

        btn_new_articel = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/editor"]')))
        btn_new_articel.click()
        time.sleep(5)

        input_article_title = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@class="form-control form-control-lg"]')))
        input_article_title.send_keys(new_article_data["article_title"])
        input_article_about = self.browser.find_element(By.XPATH, '//input[@class="form-control"]')
        input_article_about.send_keys(new_article_data["article_about"])
        input_article = self.browser.find_element(By.XPATH, '//textarea[@class="form-control"]')
        input_article.send_keys(new_article_data["article"])
        input_article_tag = self.browser.find_element(By.XPATH, '//input[@placeholder="Enter tags"]')
        input_article_tag.send_keys(new_article_data["article_tags"])

        btn_publish = self.browser.find_element(By.XPATH, '//button[@type="submit"]')
        btn_publish.click()
        time.sleep(5)

        actual_article_title = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        # print(actual_article_title.text)
        actual_article_author = self.browser.find_element(By.XPATH, '//a[@class="author"]')
        actual_article = self.browser.find_element(By.TAG_NAME, 'p')
        # print(actual_article.text)
        actual_article_tags = self.browser.find_element(By.XPATH, '//div[@class="tag-list"]')
        # print(actual_article_tags.text)
        btn_post_comment = self.browser.find_element(By.XPATH, '//button[@class="btn btn-sm btn-primary"]')

        assert actual_article_title.text == new_article_data["article_title"]
        assert actual_article_author.text == sign_up_user["username"]
        assert actual_article.text == new_article_data["article"]
        assert actual_article_tags.text == new_article_data["article_tags"]
        assert btn_post_comment.is_enabled()

        TestConduit.article_counter += 1
        # print(TestConduit.article_counter)

    @allure.id('TC7')
    @allure.title('Ismételt és sorozatos adatbevitel adatforrásból - Helyes adatokkal')
    def test_import_datas_from_file(self):
        independent_cookies_accept(self.browser)
        independent_login(self.browser)

        input_article_titles = []
        # print(self.article_counter)
        with open('./vizsgaremek/test/datas_for_conduit.csv', 'r', encoding='UTF-8') as datas:  # github actionhöz kell
            # with open('datas_for_conduit.csv', 'r') as datas: # pycharm futáshoz kell
            data_reader = csv.reader(datas, delimiter=';')
            for data in data_reader:
                btn_new_articel = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//a[@href="#/editor"]')))
                btn_new_articel.click()
                time.sleep(5)

                input_article_title = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@class="form-control form-control-lg"]')))
                input_article_about = self.browser.find_element(By.XPATH, '//input[@class="form-control"]')
                input_article = self.browser.find_element(By.XPATH, '//textarea[@class="form-control"]')
                input_article_tag = self.browser.find_element(By.XPATH, '//input[@placeholder="Enter tags"]')

                input_article_title.send_keys(data[0])
                input_article_about.send_keys(data[1])
                input_article.send_keys(data[2])
                input_article_tag.send_keys(data[3])

                input_article_titles.append(data[0])

                btn_publish = self.browser.find_element(By.XPATH, '//button[@type="submit"]')
                btn_publish.click()
                time.sleep(5)

                TestConduit.article_counter += 1
                # print(TestConduit.article_counter)

                actual_article_title = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'h1')))
                actual_article_author = self.browser.find_element(By.XPATH, '//a[@class="author"]')
                actual_article = self.browser.find_element(By.TAG_NAME, 'p')
                actual_article_tags = self.browser.find_element(By.XPATH, '//div[@class="tag-list"]')
                btn_post_comment = self.browser.find_element(By.XPATH, '//button[@class="btn btn-sm btn-primary"]')

                assert actual_article_title.text == data[0]
                assert actual_article_author.text == sign_up_user["username"]
                assert actual_article.text == data[2]
                assert actual_article_tags.text == data[3]
                assert btn_post_comment.is_enabled()

        # print(input_article_titles)

        time.sleep(5)
        # btn_menu_logged_in_user = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[3]
        # btn_menu_logged_in_user = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, f'//a[@href="#/@{sign_up_user["username"]}"]')))
        # btn_menu_logged_in_user.click()
        btn_article_author = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@class="author"]')))
        btn_article_author.click()
        time.sleep(5)

        actual_article_elements = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "h1")))
        assert len(actual_article_elements) == TestConduit.article_counter
        input_article_titles.append(new_article_data["article_title"])  # github actionhöz kell
        for article in actual_article_elements:
            assert article.text in input_article_titles

    @allure.id('TC8')
    @allure.title('Meglévő adat módosítás')
    def test_data_update(self):
        independent_cookies_accept(self.browser)
        independent_login(self.browser)
        time.sleep(2)

        btn_menu_logged_in_user = \
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[
                2]
        btn_menu_logged_in_user.click()
        time.sleep(2)

        # actual_article_elements = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.TAG_NAME, "h1")))
        update_article = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, f'//h1[text()="{new_article_data["article_title"]}"]')))
        # print(update_article.text)
        update_article.click()
        time.sleep(2)
        btn_edit_article = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@class="btn btn-sm btn-outline-secondary"]')))
        btn_edit_article.click()
        time.sleep(2)

        input_article_about = self.browser.find_element(By.XPATH, '//input[@class="form-control"]')
        input_article_about.clear()
        input_article_about.send_keys(update_article_data["article_about"])

        btn_publish = self.browser.find_element(By.XPATH, '//button[@type="submit"]')
        btn_publish.click()
        time.sleep(5)

        btn_menu_logged_in_user2 = \
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[
                3]
        btn_menu_logged_in_user2.click()
        time.sleep(2)

        update_expected_article_title = new_article_data["article_title"].lower()
        # print(update_expected_article_title)
        words_of_update_expected_article_title = update_expected_article_title.split(' ')
        new_update_expected_article_title = '-'.join(words_of_update_expected_article_title)
        actual_article_about = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, f'//a[@href="#/articles/{new_update_expected_article_title}"]/p')))
        assert actual_article_about.text != new_article_data["article_about"]
        assert actual_article_about.text == update_article_data["article_about"]

    @allure.id('TC9')
    @allure.title('Adat vagy adatok törlése')
    def test_delete_data(self):
        independent_cookies_accept(self.browser)
        independent_login(self.browser)
        time.sleep(2)

        btn_menu_logged_in_user = \
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[
                2]
        btn_menu_logged_in_user.click()
        time.sleep(2)
        self.browser.refresh()
        time.sleep(2)

        start_article_titles = []
        start_article_elements = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//h1')))
        start_number_of_article = len(start_article_elements)
        for article in start_article_elements:
            start_article_titles.append(article.text)
        # print(start_article_titles)
        assert start_number_of_article == TestConduit.article_counter
        assert new_article_data["article_title"] in start_article_titles
        delete_article = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, f'//h1[text()="{new_article_data["article_title"]}"]')))
        # print(delete_article.text)
        TestConduit.article_counter -= 1
        delete_article.click()
        time.sleep(2)

        btn_delete_article = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-outline-danger btn-sm"]')))
        btn_delete_article.click()
        time.sleep(2)

        btn_menu_logged_in_user2 = \
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[
                2]
        btn_menu_logged_in_user2.click()
        time.sleep(2)
        self.browser.refresh()
        time.sleep(5)

        after_delete_article_elements = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//h1')))
        # print(after_delete_article_elements)
        after_delete_number_of_article = len(after_delete_article_elements)
        # print(after_delete_number_of_article)
        after_delete_article_titles = []
        for article in after_delete_article_elements:
            after_delete_article_titles.append(article.text)
        # print(after_delete_article_titles)
        assert after_delete_number_of_article == start_number_of_article - 1
        assert after_delete_number_of_article == TestConduit.article_counter
        assert not new_article_data["article_title"] in after_delete_article_titles

    @allure.id('TC10')
    @allure.title('Adatok lementése felületről')
    def test_save_data_from_site(self):
        independent_cookies_accept(self.browser)
        independent_login(self.browser)
        logged_in_user_site_from_home(self.browser)
        article_titles = []
        article_abouts = []
        article_fields = []
        article_tags = []
        article_webelements = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//h1')))
        # print(article_webelements)
        number_of_article = len(article_webelements)
        # print(number_of_article)
        article_about_webelements = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//p')))
        article_tag_webelements = self.browser.find_elements(By.XPATH, '//div[@class="tag-list"]')
        p = 1
        n = 0
        for article in article_webelements:
            article_titles.append(article.text)
            # print(article_titles)
            article_abouts.append(article_about_webelements[p].text)
            # print(article_abouts)
            p += 1
            article_tags.append(article_tag_webelements[n].text)
        # print(article_titles)
        # print(article_abouts)
        # print(article_tags)

        for n in range(number_of_article):
            article_webelements = WebDriverWait(self.browser, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, '//h1')))
            article_webelements[n].click()
            time.sleep(2)
            article_field = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//p')))
            article_fields.append(article_field.text)
            logged_in_user_site_from_article(self.browser)

        # print(article_fields)
        with open('./vizsgaremek/test/datas_from_site.csv', 'w', encoding='UTF-8') as file:
            for r in range(number_of_article):
                file.write(article_titles[r])
                file.write(';')
                file.write(article_abouts[r])
                file.write(';')
                file.write(article_fields[r])
                file.write(';')
                file.write(article_tags[r])
                if r == number_of_article - 1:
                    pass
                else:
                    file.write('\n')

        with open('./vizsgaremek/test/datas_from_site.csv', 'r', encoding='UTF-8') as from_site:
            from_site_datas = csv.reader(from_site, delimiter=';')
            r = 0
            for row in from_site_datas:
                assert row[0] == article_titles[r]
                assert row[1] == article_abouts[r]
                assert row[2] == article_fields[r]
                assert row[3] == article_tags[r]
                r += 1

        with open('./vizsgaremek/test/datas_from_site.csv', 'r', encoding='UTF-8') as from_site:
            from_site_datas = csv.reader(from_site, delimiter=';')
            with open('./vizsgaremek/test/datas_for_conduit.csv', 'r', encoding='UTF-8') as for_site:
                for_site_datas = csv.reader(for_site, delimiter=';')
                # r = 0
                # for row in for_site_datas:
                #     assert for_site.readlines(r) == from_site.readlines(r)
                #     r += 1
                assert for_site.read() == from_site.read()

    @allure.id('TC11')
    @allure.title('Adatok listázása')
    def test_data_listing(self):
        independent_cookies_accept(self.browser)
        independent_login(self.browser)

        start_article_author_elements = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="author"]')))
        start_article_authors_number = 0
        for article in start_article_author_elements:
            if article.text == sign_up_user["username"]:
                start_article_authors_number += 1
        # print(start_article_authors_number)

        logged_in_user_site_from_home(self.browser)

        article_author_elements = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//a[@class="author router-link-exact-active router-link-active"]')))
        article_elements = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//h1')))
        assert len(article_author_elements) == len(article_elements)
        assert len(article_author_elements) == start_article_authors_number
        assert len(article_author_elements) == TestConduit.article_counter

    @allure.id('TC12')
    @allure.title('Több oldalas lista bejárása')
    def test_data_page_turning(self):
        independent_cookies_accept(self.browser)
        independent_login(self.browser)
        create_more_articles(self.browser)  # pycharm futtatásnál ki kell venni

        pagination_webelement = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//ul[@class="pagination"]')))
        page_number = int(pagination_webelement.text[-1])

        btn_page_numbers = self.browser.find_elements(By.XPATH, '//nav/ul/li/a')
        n = 0
        for page in btn_page_numbers:
            page.click()
            btn_page_numbers_class = self.browser.find_elements(By.XPATH, '//nav/ul/li')[n]
            assert btn_page_numbers_class.get_attribute('class') == "page-item active"
            n += 1
            # print(page.text)
        btn_page_number = len(btn_page_numbers)
        assert page_number == btn_page_number
