import time
from playwright.sync_api import sync_playwright
from conftest import db_session
from pages.page_profile import CinescopeProfilePage


class TestProfilePage:
    def test_login_by_ui(self, common_user, db_session):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()
            profile_page = CinescopeProfilePage(page)

            profile_page.open()
            profile_page.login(common_user.email, common_user.password)

            profile_page.profile()
            profile_page.check_profile(email=common_user.email, db_session=db_session)

            time.sleep(5)
            browser.close()