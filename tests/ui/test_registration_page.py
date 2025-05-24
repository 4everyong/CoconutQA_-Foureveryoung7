import time
import allure
import pytest
from playwright.sync_api import sync_playwright
from models.page_object_models import CinescopeRegisterPage
from utils.data_generator import DataGenerator


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:
   @allure.title("Проведение успешной регистрации")
   def test_register_by_ui(self):
      with sync_playwright() as playwright:
        random_email = DataGenerator.generate_random_email()
        randome_name = DataGenerator.generate_random_name()
        random_password = DataGenerator.generate_random_password()

        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        register_page = CinescopeRegisterPage(page)

        register_page.open()
        register_page.register(f"PlaywrightTest {randome_name}", random_email, random_password, random_password)

        register_page.assert_was_redirect_to_login_page()
        register_page.make_screenshot_and_attach_to_allure()
        register_page.assert_allert_was_pop_up()

        time.sleep(5)
        browser.close()