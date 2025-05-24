from playwright.sync_api import Page
from pages.base_page import BasePage


class CinescopLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}login"

        self.email_input = self.page.get_by_role("textbox", name="Email")
        self.password_input = self.page.get_by_role("textbox", name="Пароль", exact=True)

        self.login_button = self.page.locator("form").get_by_role("button", name="Войти")
        self.register_button = self.page.get_by_role("button", name="Зарегистрироваться")

    def open(self):
        self.open_url(self.url)

    def login(self, email: str, password: str):
        self.enter_text_to_element(self.email_input,email)
        self.enter_text_to_element(self.password_input, password)
        self.click_element(self.login_button)

    def assert_was_redirect_to_home_page(self):
        self.wait_redirect_for_url(self.home_url)

    def assert_allert_was_pop_up(self):
        self.check_pop_up_element_with_text("Вы вошли в аккаунт")