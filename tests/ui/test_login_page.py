import time

import allure
import pytest
from playwright.sync_api import sync_playwright
from conftest import common_user
from models.page_object_models import CinescopLoginPage


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestloginPage:
   @allure.title("Проведение успешного входа в систему")
   def test_login_by_ui(self, common_user):
      with sync_playwright() as playwright:
          browser = playwright.chromium.launch(headless=False)
          page = browser.new_page()
          login_page = CinescopLoginPage(page)

          login_page.open()
          login_page.login(common_user.email, common_user.password)

          login_page.assert_was_redirect_to_home_page()
          login_page.make_screenshot_and_attach_to_allure()
          login_page.assert_allert_was_pop_up()

          time.sleep(5)
          browser.close()