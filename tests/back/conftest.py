import pytest
import requests
from api.api_manager import ApiManager
from constants import HEADERS
from utils.data_generator import DataGenerator


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

@pytest.fixture(scope='function')
def data_film():
    film_name = DataGenerator.generate_random_film()
    film_image_url = DataGenerator.generate_random_image_url()
    price = DataGenerator.generate_random_price()
    description = DataGenerator.generate_random_description()
    location = DataGenerator.generate_random_location()
    published = DataGenerator.generate_random_published()
    genre_id = DataGenerator.generate_random_genre_id()
    return {
          "name": film_name,
          "imageUrl": film_image_url,
          "price": price,
          "description": description,
          "location": location,
          "published": published,
          "genreId": genre_id
        }

@pytest.fixture(scope='function')
def data_film_min():
    film_name = DataGenerator.generate_random_film()
    price = DataGenerator.generate_random_price()
    description = DataGenerator.generate_random_description()
    location = DataGenerator.generate_random_location()
    published = DataGenerator.generate_random_published()
    genre_id = DataGenerator.generate_random_genre_id()
    return {
        "name": film_name,
        "price": price,
        "description": description,
        "location": location,
        "published": published,
        "genreId": genre_id
    }

@pytest.fixture(scope="function")
def create_delete_film(api_manager, data_film):
    response = api_manager.movies_api.create_movie(movie_data=data_film)
    response_data= response.json()
    id_film = response_data.get("id")
    yield response_data
    api_manager.movies_api.delete_movie(id_film)
    api_manager.movies_api.get_movies_by_id(movie_id=id_film, expected_status=404)

@pytest.fixture(scope="function")
def create_film(api_manager, data_film):
    response = api_manager.movies_api.create_movie(movie_data=data_film)
    return response.json()


