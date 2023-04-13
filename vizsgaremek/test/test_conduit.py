import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from datetime import time
import allure
import csv
import time

from data_conduit import sign_up_user, btns_menu_logged_in_expected_text, btns_menu_logged_out_expected_text, \
    new_article_data, update_article_data
from module_conduit import independent_cookies_accept, independent_login, logged_in_user_site_from_home, \
    logged_in_user_site_from_article, create_more_articles_from_file, go_home, list_upload, btn_publish, \
    btn_new_articel, input_new_article


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
        self.browser.quit()

    @allure.id('TC1')
    @allure.title('Oldal megnyitása')
    @allure.description('''
    Teszteset leírás:
    
        Conduit weboldal megnyitása.
    
    Vizsgálat leírás:
    
        - az oldalon a weboldal neve megjelenik
        - az oldalon a weboldal logoja megjelenik
        - az oldalon a weboldal neve conduit
        - az oldalon a weboldal logojának a szövege conduit
    ''')
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
    @allure.description('''
    Teszteset leírás:
   
        Conduit weboldal adatkezelési nyilatkozat panelnek és az elfogadó gombnak a megkeresése. Majd a gomb 
        megnyomása.
   
    Vizsgálat leírás:
   
        - a nyilatkozat elfogadása előtt:
            < az adatkeezlési nyilatkozat panel az oldalon megjelenik és interaktálható
            < a nyilatkozatot elfogadó gomb a panelen használható
   
        - a nyilatkozat elfogadása után: 
            < az adatkezelési nyilatkozat panel nem jelenik meg, megkeresése hibát ad
        ''')
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
    @allure.description('''
    Teszteset leírás:
    
        Másik modulból adatkezelési nyilatkozat elfogadása függvény behívása.
        Regisztráció menü megkeresése és megnyomása.
        Input mezők megkeresése és külső data fájlból adatokkal történő kitöltése.
        Regisztráció gomb megkeresése és megnyomása.
        Megjelenő válaszpanel üzenetének és ok gombjának megkeresése. Majd gomb megnyomása.
    
    Vizsgálatok leírása:
        
        - regisztráció gomb megnyomása előtt:
            < az input mezők nem üresek
            < az input mezőkben azok az adatok szerepelnek, amik a külső adatforrásban is megjelennek
        
        - regisztráció gomb megnyomása után:
            < a kapott válasz üzenet szövegének ellenőrzése
            < a válaszüzeneten lévő ok gomb interaktálható    
    ''')
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
        time.sleep(2)
        message_ok = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="swal-text"]')))
        assert message_ok.text == 'Your registration was successful!'
        btn_ok_sign_up = self.browser.find_element(By.XPATH, '//button[@class="swal-button swal-button--confirm"]')
        assert btn_ok_sign_up.is_enabled()
        btn_ok_sign_up.click()

    @allure.id('TC4')
    @allure.title('Bejelentkezés - Helyes adatokkal')
    @allure.description('''
    Teszteset leírás:
    
        Másik modulból adatkezelési nyilatkozat elfogadása függvény behívása.
        Bejelentkezési menü megkeresése és megnyomása.
        Input mezők megkeresése és külső data fájlból adatokkal történő kitöltése.
        Bejelentkezés gomb megkeresése és megnyomása.
        Bejelentkezett felhasználó menüpontjának megkeresése.
        A bejelentkezést követően az újonnan megjelenő menüpontok megkeresése.
    
    Vizsgálatok leírása:
    
        - bejelentkezés gomb megnyomása előtt:
            < a bejelentkezési gomb használható
            < az input mezők nem üresek
            < az input mezőkben azok az adatok szerepelnek, amik a külső adatforrásban is megjelennek
    
        - bejelentkezési gomb megnyomása után:
            < megjelenik a felhasználói menüpont
            < a felhasználói menüpont interaktálható
            < a felhasználói menüpont szövege megegyezik a külső data forrásban szereplő szöveggel
            < a megjelenő menüpontok szövegei megegyeznek a külső data forrásban szereplő szövegekkel
    ''')
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
        time.sleep(2)
        btn_menu_logged_in_user = \
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[
                2]
        assert btn_menu_logged_in_user.is_displayed()
        assert btn_menu_logged_in_user.is_enabled()
        assert btn_menu_logged_in_user.text == sign_up_user['username']
        btns_menu_new = self.browser.find_elements(By.XPATH, '//a[@class="nav-link"]')
        n = 0
        for btn in btns_menu_new:
            assert btn.text == btns_menu_logged_in_expected_text[n]
            n += 1

    @allure.id('TC5')
    @allure.title('Kijelentkezés - Helyes adatokkal')
    @allure.description('''
    Teszteset leírás:
    
        Másik modulból meghívott függvények: 
            - adatkezelési nyilatkozat elfogadása
            - bejelentkezés megadott felhasználóval
    
        Kijelentkezési menü megkeresése és megnyomása.
        A kijelentkezést követően az újonnan megjelenő menüpontok megkeresése.
    
    Vizsgálatok leírása:
    
        - az oldalon a weboldal neve megjelenik
        - az oldalon a weboldal logoja megjelenik
        - az oldalon a weboldal neve conduit
        - az oldalon a weboldal logojának a szövege conduit
        - a megjelenő menüpontok szövegei megegyeznek a külső data forrásban szereplő szövegekkel
    ''')
    def test_log_out(self):
        independent_cookies_accept(self.browser)
        independent_login(self.browser)

        btn_menu_log_out = \
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[
                3]
        btn_menu_log_out.click()
        time.sleep(2)

        page_name = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//a[@class="navbar-brand router-link-exact-active router-link-active"]')))
        logo_name = self.browser.find_element(By.XPATH, '//h1[@class="logo-font"]')
        assert page_name.is_displayed()
        assert logo_name.is_displayed()
        assert page_name.text == "conduit"
        assert logo_name.text == "conduit"

        btns_menu_logged_out = self.browser.find_elements(By.XPATH, '//li[@class="nav-item"]')
        n = 0
        for btn in btns_menu_logged_out:
            assert btn.text == btns_menu_logged_out_expected_text[n]
            n += 1

    @allure.id('TC6')
    @allure.title('Új adat bevitel (blogbejegyzés) - Helyes adatokkal')
    @allure.description('''
    Teszteset leírás:
    
        Másik modulból meghívott függvények: 
            - adatkezelési nyilatkozat elfogadása
            - bejelentkezés megadott felhasználóval
            - új cikk létrehozása menü megkeresése és átnavigálás
            - új cikk adatainak kitöltése
            - cikk publikálása
    
        Új blogbejegyzés menü megkeresése és megnyomása.
        Input mezők megkeresése és külső data fájlból adatokkal történő kitöltése.
        Publikálás gomb megkeresése és megnyomása.
        Az újonnan megjelenő oldalon a létrehozott blogbejegyzés adatainak megkeresése.
        Új komment létrehozás gomb megkeresése.
        Felhasználó által létrehozott blogbejegyzések számolásához létrehozott osztályváltozó értékének 1-gyel 
        történő növelése.
    
    Vizsgálatok leírása:
    
        - a létrehozott blogbejegyzés adatainak szövege megegyezik a külső forrásban lévő adatok szövegével
        - új komment létrehozása gomb interaktárlható
    ''')
    def test_data_creation(self):
        independent_cookies_accept(self.browser)
        independent_login(self.browser)
        btn_new_articel(self.browser)
        input_new_article(self.browser, new_article_data["article_title"], new_article_data["article_about"],
                          new_article_data["article"], new_article_data["article_tags"])
        btn_publish(self.browser)

        actual_article_title = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        actual_article_author = self.browser.find_element(By.XPATH, '//a[@class="author"]')
        actual_article = self.browser.find_element(By.TAG_NAME, 'p')
        actual_article_tags = self.browser.find_element(By.XPATH, '//div[@class="tag-list"]')
        btn_post_comment = self.browser.find_element(By.XPATH, '//button[@class="btn btn-sm btn-primary"]')

        assert actual_article_title.text == new_article_data["article_title"]
        assert actual_article_author.text == sign_up_user["username"]
        assert actual_article.text == new_article_data["article"]
        assert actual_article_tags.text == new_article_data["article_tags"]
        assert btn_post_comment.is_enabled()

        TestConduit.article_counter += 1

    @allure.id('TC7')
    @allure.title('Ismételt és sorozatos adatbevitel adatforrásból (blogbejegyzések) - Helyes adatokkal')
    @allure.description('''
    Teszteset leírás:
        
        Másik modulból meghívott függvények: 
            - adatkezelési nyilatkozat elfogadása
            - bejelentkezés megadott felhasználóval
            - felhasználói menübe navigálás (blogbejegyzésből)
            - új cikk létrehozása menü megkeresése és átnavigálás
            - új cikk adatainak kitöltése
            - cikk publikálása
        
        Függvény válozó létrehozása a teszteset során létrehozott blogbejegyzések címének eltárolásához.
        Külső adatforrás megnyitása
        For ciklusban: 
            Új blogbejegyzés menü megkeresése és megnyomása.
            Input mezők megkeresése és külső data fájlból adatokkal történő kitöltése.
            Függvény változóhoz hozzáadásra kerül a létrehozott blogbejegyzés címe
            Publikálás gomb megkeresése és megnyomása.
            Felhasználó által létrehozott blogbejegyzések számolásához létrehozott osztályváltozó értékének 
            1-gyel történő növelése.
            Az újonnan megjelenő oldalon a létrehozott blogbejegyzés adatainak megkeresése.
            Új komment létrehozás gomb megkeresése.
        Felhasználói menübe nevigálás.
        Az oldalon a felhasználóhoz tartozó blogbejegyzések címeinek kikeresése.
        A TC6-ban létrehozott blogbejegyzés címének hozzáadása a függvény változóhoz.
    
    Vizsgálatok leírása:
    
        - for cikluson belül:
            < a létrehozott blogbejegyzés adatainak szövege megegyezik a külső forrásban lévő adatok 
              szövegével
            < új komment létrehozása gomb interaktárlható
    
        - for ciklus után:
            < az oldalon a felhasználóhoz tartozó blogbejegyzések címeinek száma megegyezik a felhasználó 
              által létrehozott blogbejegyzések osztályváltozóban tárolt értékével
            < a függvény változóban eltárolt blogbejegyzés címek lista elemei szerepelnek a felhasználói 
              menüpont alatt megjelenő felhasználóhoz tartozó bejegyzések címeinek listájában
    ''')
    def test_import_datas_from_file(self):
        independent_cookies_accept(self.browser)
        independent_login(self.browser)

        input_article_titles = []
        with open('./vizsgaremek/test/datas_for_conduit.csv', 'r', encoding='UTF-8') as datas:
            data_reader = csv.reader(datas, delimiter=';')
            for data in data_reader:
                btn_new_articel(self.browser)
                input_new_article(self.browser, data[0], data[1], data[2], data[3])
                btn_publish(self.browser)

                input_article_titles.append(data[0])

                TestConduit.article_counter += 1

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

        logged_in_user_site_from_article(self.browser)

        actual_article_elements = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "h1")))
        assert len(actual_article_elements) == TestConduit.article_counter
        input_article_titles.append(new_article_data["article_title"])
        for article in actual_article_elements:
            assert article.text in input_article_titles

    @allure.id('TC8')
    @allure.title('Meglévő adat módosítás (blogbejegyzés About mező')
    @allure.description('''
    Teszteset leírás:
    
        Másik modulból meghívott függvények: 
            - adatkezelési nyilatkozat elfogadása
            - bejelentkezés megadott felhasználóval
            - felhasználói menübe navigálás (home oldalról)
            - felhasználói menübe navigálás (blogbejegyzésből)
            - cikk publikálása
            
        Módosítani kívánt blogbejegyzés megkeresése (külső adatforrás segítségévle) és megjelenítése.
        Blogbejegyzés módosítása gomb megkeresése és megnyomása
        Bejegyzés About mezőjének megkeresése, tartalmának törlése és külső adatforrásból az új értékkel 
        történő kitöltése.
        Publikálás gomb megkeresése és megnyomása.
        Felhasználói menübe navigálás
        A módosított bejegyzés címének a formátumának az átalakítása.
        Az átalakított cím segítségével a módosított blogbejegyzés About mezőjének kikeresése.
    
    Vizsgálatok leírása:
    
        - a módosított bejegyzés About mezőjének jelenlegi értéke nem egyezik meg a külső adatforrásban 
          szereplő eredeti About mező szöveg értékével
        - a módosított bejegyzés About mezőjének jelenlegi értéke megegyezik a külső adatforrásban szereplő 
          módosított About mező szöveg értékével
    ''')
    def test_data_update(self):
        independent_cookies_accept(self.browser)
        independent_login(self.browser)
        logged_in_user_site_from_home(self.browser)
        time.sleep(2)

        update_article = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, f'//h1[text()="{new_article_data["article_title"]}"]')))
        update_article.click()
        time.sleep(2)
        btn_edit_article = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@class="btn btn-sm btn-outline-secondary"]')))
        btn_edit_article.click()
        time.sleep(2)

        input_article_about = self.browser.find_element(By.XPATH, '//input[@class="form-control"]')
        input_article_about.clear()
        input_article_about.send_keys(update_article_data["article_about"])

        btn_publish(self.browser)

        logged_in_user_site_from_article(self.browser)

        update_expected_article_title = new_article_data["article_title"].lower()
        words_of_update_expected_article_title = update_expected_article_title.split(' ')
        new_update_expected_article_title = '-'.join(words_of_update_expected_article_title)
        actual_article_about = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, f'//a[@href="#/articles/{new_update_expected_article_title}"]/p')))
        assert actual_article_about.text != new_article_data["article_about"]
        assert actual_article_about.text == update_article_data["article_about"]

    @allure.id('TC9')
    @allure.title('Adat vagy adatok törlése (blogbejegyzés)')
    @allure.description('''
    Teszteset leírás:
    
        Másik modulból meghívott függvények: 
            - adatkezelési nyilatkozat elfogadása
            - bejelentkezés megadott felhasználóval
            - felhasználói menübe navigálás (home oldalról)
            - lista feltöltése adatokkal
    
        Függvény válozó létrehozása a törlés előtt meglévő felhasználóhoz taroztó blogbejegyzések címének 
        eltárolásához.
        A felhasználóhoz tartozó bejegyzések címeinek kikeresése.
        A címek számának eltárolása egy függvény vátlozóba.
        For ciklus segítségével a törlsé előtti start állapot szerinti bejegyzés címek tárolására létrehozott 
        függvény változó feltöltése.
        Törölni kívánt blogbejegyzés megkeresése (külső adatforrás segítségévle) és megjelenítése.
        Blogbejegyzés törlése gomb megkeresése és megnyomása
        Felhasználó által létrehozott blogbejegyzések számolásához létrehozott osztályváltozó értékének 1-gyel 
        történő csökkentése.
        Felhasználói menübe navigálás
        Függvény válozó létrehozása a törlés utáni felhasználóhoz taroztó blogbejegyzések címének 
        eltárolásához.
        A törlés után a felhasználóhoz tartozó bejegyzések címeinek kikeresése.
        A törlés után a címek számának eltárolása egy függvény változóba.
        For ciklus segítségével a törlsé utáni állapot szerinti bejegyzés címek tárolására létrehozott 
        függvény változó feltöltése.
        
    Vizsgálatok leírása:
    
        - törlés előtt:
            < az oldalon a felhasználóhoz tartozó blogbejegyzések címeinek száma megegyezik a felhasználó 
              által létrehozott blogbejegyzések osztályváltozóban tárolt értékével
            < a függvény változóban eltárolt blogbejegyzés címek lista elemei szerepelnek a felhasználói m
              enüpont alatt megjelenő felhasználóhoz tartozó bejegyzések címeinek listájában
    
        - törlés után:
            < a törlés utáni felhasználóhoz taroztó cikkek száma megegyezik a törlés előtti felhasználóhoz 
              tartozó cikkek számának eggyel csökkentett értékével
            < a törlés utáni felhasználóhoz taroztó cikkek száma megegyezik a felhasználó által létrehozott 
              blogbejegyzések osztályváltozóban tárolt értékével
            < törölt blogbejegyzés címe nem szerepel a törlés utáni felhasználóhoz tartozó cikkek címének 
              listájában
    ''')
    def test_delete_data(self):
        independent_cookies_accept(self.browser)
        independent_login(self.browser)
        logged_in_user_site_from_home(self.browser)

        start_article_titles = []
        start_article_elements = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//h1')))
        start_number_of_article = len(start_article_elements)
        list_upload(start_article_elements, start_article_titles)
        assert start_number_of_article == TestConduit.article_counter
        assert new_article_data["article_title"] in start_article_titles
        delete_article = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, f'//h1[text()="{new_article_data["article_title"]}"]')))
        TestConduit.article_counter -= 1
        delete_article.click()
        time.sleep(2)

        btn_delete_article = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-outline-danger btn-sm"]')))
        btn_delete_article.click()
        time.sleep(2)

        logged_in_user_site_from_home(self.browser)
        time.sleep(2)

        after_delete_article_elements = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//h1')))
        after_delete_number_of_article = len(after_delete_article_elements)
        after_delete_article_titles = []
        list_upload(after_delete_article_elements, after_delete_article_titles)
        assert after_delete_number_of_article == start_number_of_article - 1
        assert after_delete_number_of_article == TestConduit.article_counter
        assert not new_article_data["article_title"] in after_delete_article_titles

    @allure.id('TC10')
    @allure.title('Adatok lementése felületről (blogbejegyzések)')
    @allure.description('''
    Teszteset leírás:

        Másik modulból meghívott függvények: 
            - adatkezelési nyilatkozat elfogadása
            - bejelentkezés megadott felhasználóval
            - felhasználói menübe navigálás (home oldalról)
            - felhasználói menübe navigálás (blogbejegyzésből)
            - lista feltöltése adatokkal

        Üres liták létrehozása, amibe lementésre kerülnek a weboldalon szereplő felhasználó által készített 
        bejegyzések különböző mezői.
        Bejegyzések mezőinek kikeresése (cím, about, tag).
        Felhasználóhoz tartozó cikkek számának meghatározsáa bejegyzés címek száma alapján.
        Első for ciklusban: 
            Az előzőekben létrehozott üres listák feltöltése adatokkal (cím, about, tag)
        Második for ciklusban:
            Az egyes bejegyzések teljes tartalmának megjelenítése.
            A bejegyzésekben lévő szöveg mezők kikeresése és a szöveg mezőket tartalmazó lista feltöltése 
            ezen adatokkal.
            Majd a felhasználói menübe nevigálás.
        Első "with' metódusban:
            Fájl létrehozása, amibe az előzőekben létrehozott listákból egy-egy sorba beírásra keülnek az 
            egy bejegyzéshez tartozó adatok ;-vel elválasztva.
        
    Vizsgálatok leírása:

        - második "with" metódusban:
            < a létrehozott fájl pontosvesszővel elválasztott elemei megegyeznek a létrehozott listák 
              megfelelő elemeivel

        - harmadik "with" metódusban:
            < a létrehozott fájl teljes tartalma megegyezik a korábbi ismételt és sorozatos adatbevitel 
              adatforrásból tesztesetnél használt adatforrással
    ''')
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
        number_of_article = len(article_webelements)
        article_about_webelements = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//p')))
        article_tag_webelements = self.browser.find_elements(By.XPATH, '//div[@class="tag-list"]')
        list_upload(article_webelements, article_titles)
        list_upload(article_tag_webelements, article_tags)
        list_upload(article_about_webelements[1:], article_abouts)

        for n in range(number_of_article):
            article_webelements = WebDriverWait(self.browser, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, '//h1')))
            article_webelements[n].click()
            time.sleep(2)
            article_field = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//p')))
            article_fields.append(article_field.text)
            logged_in_user_site_from_article(self.browser)

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
                assert for_site.read() == from_site.read()

    @allure.id('TC11')
    @allure.title('Adatok listázása (adott felhasználó által létrehozott blogbejegyzések)')
    @allure.description('''
    Teszteset leírás:

        Másik modulból meghívott függvények: 
            - adatkezelési nyilatkozat elfogadása
            - bejelentkezés megadott felhasználóval
            - felhasználói menübe navigálás (home oldalról)

        A bejelentkezést követő oldalon megjelenő összes cikk szerző elemének kikeresése.
        Egy függvényváltozó létrehozása, melyben a bejelentkezett felhasználó által készített cikkek 
        száma kerül eltárolásra.
        Első for ciklusban: 
            Ha a vizsgált szerző text adata megegyezik a bejelentkezett felhasználó username adatával, 
            akkor a létrehozott függvényváltozó értéke megnövekszik 1-gyel
        Felhasználói menübe navigálás. 
        Megjelennek a felhasználó által készített cikkek listája.
        A megjelent cikkek szerző adatainak kikeresése.
        A megjelent cikkek cím adatainak megkeresése.

    Vizsgálatok leírása:

        - A felhasználói menüben megjelenő cikkek szerző adatainak száma megegyezik az ezen az oldalon 
          szereplő cikk címek számával.
        - A felhasználói menüben megjelenő cikkek szerző adatainak száma megegyezik a korábban 
          létrehozott függvényváltozó (bejelentkezett felhasználó által készített cikkek száma a 
          nyitóoldalon, szűrés nélkül) értékével
        - A felhasználói menüben megjelenő cikkek szerző adatainak száma megegyezik a felhasználó 
          által létrehozott blogbejegyzések osztályváltozóban tárolt értékével
    ''')
    def test_data_listing(self):
        independent_cookies_accept(self.browser)
        independent_login(self.browser)

        start_article_author_elements = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="author"]')))
        start_article_authors_number = 0
        for article in start_article_author_elements:
            if article.text == sign_up_user["username"]:
                start_article_authors_number += 1

        logged_in_user_site_from_home(self.browser)

        article_author_elements = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//a[@class="author router-link-exact-active router-link-active"]')))
        assert len(article_author_elements) == start_article_authors_number
        assert len(article_author_elements) == TestConduit.article_counter

    @allure.id('TC12')
    @allure.title('Több oldalas lista bejárása (blogbejegyzések bejárása Home/Global feed oldalon)')
    @allure.description('''
    Teszteset leírás:

        Másik modulból meghívott függvények: 
            - adatkezelési nyilatkozat elfogadása
            - bejelentkezés megadott felhasználóval
            - tömeges blogbejegyzés létrehozás külső adatforrásból
            - Home oldalra navigálás
            - felhasználói menübe navigálás (home oldalról)

        A Home/Global feed menü alatt megjelennek a webhelyen a létrehozott blogbejegyzések szűrő 
        használata nélkül.
        A lapozásra vonatkozó összesítő webelement kikeresése.
        Az összesítő utolsó elemének eltárolása egy függvényváltozóba. Ez adja meg az utolsó oldal 
        számát.
        Az oldlak számainak kikeresése a webhelyen.
        For ciklusban: 
            Az oldal lap számra kattintás.
            Az aktív oldal class attribútumának kikeresése.
        Függvényváltozóba rögzítésre kerül az oldalak számainak mennyisége.

    Vizsgálatok leírása:

        - For cikluson belül:
            < A megkattintott oldal class attribútuma megegyezik a "page-item active" classal. 
            < A következő oldal class attribútuma nem egyezik meg a "page-item active" classal.
        - For ciklus után:
            < Az oldalak számának mennyisége megegyezik a lapok összesítőjének utolsó értékével
    ''')
    def test_data_page_turning(self):
        independent_cookies_accept(self.browser)
        independent_login(self.browser)
        create_more_articles_from_file(self.browser, './vizsgaremek/test/datas_for_page_turning_conduit.csv')
        go_home(self.browser)

        pagination_webelement = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//ul[@class="pagination"]')))
        page_number = int(pagination_webelement.text[-1])

        btn_page_numbers = self.browser.find_elements(By.XPATH, '//nav/ul/li/a')
        n = 0
        btn_page_number = len(btn_page_numbers)
        for page in btn_page_numbers:
            page.click()
            btn_page_numbers_class = self.browser.find_elements(By.XPATH, '//nav/ul/li')[n]
            assert btn_page_numbers_class.get_attribute('class') == "page-item active"
            if n == btn_page_number - 1:
                pass
            else:
                assert self.browser.find_elements(By.XPATH, '//nav/ul/li')[n + 1].get_attribute(
                    'class') != "page-item active"
            n += 1
        assert page_number == btn_page_number
