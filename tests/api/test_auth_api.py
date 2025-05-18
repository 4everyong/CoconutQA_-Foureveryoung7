from api.api_manager import ApiManager
from models.base_models import RegisterUserResponse


class TestAuth:
    def test_register_user(self, test_user, api_manager: ApiManager):
        response = api_manager.auth_api.register_user(test_user)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"
