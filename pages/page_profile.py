from playwright.sync_api import Page
from conftest import db_session
from db_requester.models import UserDBModel
from pages.base_page import BasePage


class CinescopeProfilePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}login"

        self.email_input = self.page.get_by_role("textbox", name="Email")
        self.password_input = self.page.get_by_role("textbox", name="Пароль", exact=True)

        self.login_button = self.page.locator("form").get_by_role("button", name="Войти")
        self.register_button = self.page.get_by_role("button", name="Зарегистрироваться")

        self.profile_button = self.page.get_by_role("button", name="Профиль")
        self.profile_id = self. page.get_by_text("ID:")
        self.profile_fio = self.page.get_by_text("ФИО:")
        self.profile_email = self.page.get_by_text("Email:")
        self.profile_role = self.page.get_by_text("Роли:")

    def open(self):
        self.open_url(self.url)

    def login(self, email: str, password: str):
        self.enter_text_to_element(self.email_input,email)
        self.enter_text_to_element(self.password_input, password)
        self.click_element(self.login_button)

    def profile(self):
        self.click_element(self.profile_button)

    def check_profile(self, email: str, db_session):
        user = db_session.query(UserDBModel).filter(UserDBModel.email == email).first()
        self.check_element(self.profile_id, user.id)
        self.check_element(self.profile_role, user.roles.strip("{}"))
        self.check_element(self.profile_email, user.email)
        self.check_element(self.profile_fio, user.full_name)
