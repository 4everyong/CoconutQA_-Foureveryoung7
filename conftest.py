import json
import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.api_manager import ApiManager
from constants.roles import Roles
from entities.user import User
from models.base_models import TestUser, FilmRequest, FilmResponse
from resources.user_creds import SuperAdminCreds
from utils.data_generator import DataGenerator


@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()
    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture(scope="function")
def creation_user_data(test_user) -> TestUser:
    updated_data = json.loads(test_user.model_dump_json())
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture(scope='session')
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope='session')
def api_manager(session):
    return ApiManager(session)

@pytest.fixture(scope='function')
def data_film():
    return FilmRequest (
          name=DataGenerator.generate_random_film(),
          imageUrl=DataGenerator.generate_random_image_url(),
          price=DataGenerator.generate_random_price(),
          description=DataGenerator.generate_random_description(),
          location=DataGenerator.generate_random_location(),
          published=DataGenerator.generate_random_published(),
          genreId=DataGenerator.generate_random_genre_id()
    )

@pytest.fixture(scope='function')
def data_film_min():
    return FilmRequest(
        name=DataGenerator.generate_random_film(),
        price=DataGenerator.generate_random_price(),
        description=DataGenerator.generate_random_description(),
        location=DataGenerator.generate_random_location(),
        published=DataGenerator.generate_random_published(),
        genreId=DataGenerator.generate_random_genre_id()
    )

@pytest.fixture(scope="function")
def create_delete_film(data_film: FilmRequest, super_admin) -> FilmResponse:
    response = super_admin.api.movies_api.create_movie(movie_data=data_film)
    response_data= FilmResponse(**response.json())
    id_film = response_data.id
    yield response_data
    super_admin.api.movies_api.delete_movie(id_film)
    super_admin.api.movies_api.get_movies_by_id(movie_id=id_film, expected_status=404)

@pytest.fixture(scope="function")
def create_film(data_film: FilmRequest, super_admin):
    response = super_admin.api.movies_api.create_movie(movie_data=data_film)
    return FilmResponse(**response.json())

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        "[SUPER_ADMIN]",
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        list(Roles.USER.value),
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

HOST = "92.255.111.76"
PORT = 31200
DATABASE_NAME = "db_movies"
USERNAME = "postgres"
PASSWORD = "AmwFrtnR2"

engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}") # Создаем движок (engine) для подключения к базе данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Создаем фабрику сессий

@pytest.fixture(scope="module")
def db_session():
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных.
    После завершения теста сессия автоматически закрывается.
    """
    # Создаем новую сессию
    db_session = SessionLocal()
    # Возвращаем сессию в тест
    yield db_session
    # Закрываем сессию после завершения теста
    db_session.close()