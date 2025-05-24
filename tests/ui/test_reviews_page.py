import time
from playwright.sync_api import sync_playwright
from conftest import create_film
from pages.page_reviews import CinescopeReviewsPage
from utils.data_generator import DataGenerator


class TestReviewsPage:
    def test_reviews_by_ui(self, common_user, create_film, db_session):
        reviews = DataGenerator.generate_reviews()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()
            reviews_page = CinescopeReviewsPage(page, reviews)

            reviews_page.open()
            reviews_page.login(common_user.email, common_user.password)

            reviews_page.go_to_all_movies()

            reviews_page.create_reviews(create_film,reviews=reviews)
            reviews_page.assert_reviews_is_visible(reviews=reviews)
            reviews_page.assert_reviews_in_db(create_film.id, db_session)

            time.sleep(5)
            browser.close()

