import pytest
import requests

from api.api_manager import ApiManager
from constants import LOGIN_ENDPOINT, HEADERS, BASE_URL
from custom_requester.custom_requester import CustomRequester

@pytest.fixture(scope='session')
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope='session')
def api_manager(auth_session):
    return ApiManager(auth_session)

@pytest.fixture(scope='session')
def auth_session(session):
    session.headers.update(HEADERS)
    response = requests.post("https://auth.dev-cinescope.coconutqa.ru/login", json={
    "email": "api1@gmail.com",
    "password": "asdqwe123Q"
})
    token = response.json().get("accessToken")
    assert token is not None, "Token is None"
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session

@pytest.fixture(scope='session')
def data_film():
    return {
          "name": "Тестовый фильм",
          "imageUrl": "https://image.url",
          "price": 1240,
          "description": "Тестовое описание",
          "location": "MSK",
          "published": True,
          "genreId": 1
        }

@pytest.fixture(scope='session')
def data_film_min():
    return {
          "name": "Тестовый фильм",
          "price": 1240,
          "description": "Тестовое описание",
          "location": "MSK",
          "published": True,
          "genreId": 1
        }