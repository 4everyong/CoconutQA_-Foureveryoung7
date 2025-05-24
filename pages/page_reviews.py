import re

from playwright.sync_api import Page

from conftest import create_film, db_session
from db_requester.models import ReviewsDBModel
from pages.base_page import BasePage


class CinescopeReviewsPage(BasePage):
    def __init__(self, page: Page, reviews):
        super().__init__(page)
        self.url = f"{self.home_url}login"

        self.email_input = self.page.get_by_role("textbox", name="Email")
        self.password_input = self.page.get_by_role("textbox", name="Пароль", exact=True)

        self.login_button = self.page.locator("form").get_by_role("button", name="Войти")
        self.register_button = self.page.get_by_role("button", name="Зарегистрироваться")

        self.reviews_input = self.page.get_by_role("textbox", name="Написать отзыв")
        self.send_button = self.page.get_by_role("button", name="Отправить")
        self.reviews_visible = self.page.get_by_text(f"{reviews}Рейтинг: 5/").first

    def open(self):
        self.open_url(self.url)

    def login(self, email: str, password: str):
        self.enter_text_to_element(self.email_input,email)
        self.enter_text_to_element(self.password_input, password)
        self.click_element(self.login_button)

    def create_reviews(self, create_film, reviews: str):
        self.open_url(f"{self.home_url}/movies/{create_film.id}")
        self.enter_text_to_element(self.reviews_input, reviews)
        self.click_element(self.send_button)

    def assert_reviews_is_visible(self, reviews: str):
        self.reviews_input.is_hidden()
        self.check_element(self.reviews_visible, reviews)

    def assert_reviews_in_db(self, movie_id, db_session):
        reviews = db_session.query(ReviewsDBModel).filter(ReviewsDBModel.movie_id == movie_id).first()
        self.check_element(self.reviews_visible, reviews.text)