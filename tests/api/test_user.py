from models.base_models import RegisterUserResponse, TestUser
from conftest import super_admin


class TestUser:

    def test_create_user(self, super_admin, creation_user_data: TestUser):
        response = super_admin.api.user_api.create_user(creation_user_data)
        register_user_response = RegisterUserResponse(**response.json())

        assert register_user_response.email == creation_user_data['email']
        assert register_user_response.fullName == creation_user_data['fullName']
        assert register_user_response.verified is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user(creation_user_data['email']).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_id.get('email') == creation_user_data['email']
        assert response_by_id.get('fullName') == creation_user_data['fullName']
        assert response_by_id.get('roles', []) == creation_user_data['roles']
        assert response_by_id.get('verified') is True