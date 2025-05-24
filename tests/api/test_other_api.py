import datetime
import uuid
import allure
import pytest
from pytz import timezone
from sqlalchemy.orm import Session
from db_requester.models import MovieDBModel, AccountTransactionTemplate, GenreDBModel
from conftest import db_session
from utils.data_generator import DataGenerator


def test_create_delete_movie(api_manager, super_admin, db_session: Session):
    # как бы выглядел SQL запрос
    """SELECT id, "name", price, description, image_url, "location", published, rating, genre_id, created_at
       FROM public.movies
       WHERE name='Test Moviej1h8qss9s5';"""

    movie_name = f"Test Movie{DataGenerator.generate_random_film()}"
    movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name)

    # проверяем что до начала тестирования фильма с таким названием нет
    assert movies_from_db.count() == 0, "В базе уже присутствует фильм с таким названием"

    movie_data = {
        "name": movie_name,
        "price": 500,
        "description": "Описание тестового фильма",
        "location": "MSK",
        "published": True,
        "genreId": 3
    }
    response = super_admin.api.movies_api.create_movie(
        movie_data=movie_data,
    )
    assert response.status_code == 201, "Фильм должен успешно создаться"
    response = response.json()

    # проверяем после вызова api_manager.movies_api.create_movie в базе появился наш фильм
    movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name)
    assert movies_from_db.count() == 1, "В базе уже присутствует фильм с таким названием"

    movie_from_db = movies_from_db.first()
    # можете обратить внимание что в базе данных етсь поле created_at которое мы не здавали явно
    # наш сервис сам его заполнил. проверим что он заполнил его верно с погрешностью в 5 минут
    assert movie_from_db.created_at >= (
                datetime.datetime.now(timezone('UTC')).replace(tzinfo=None) - datetime.timedelta(
            minutes=5)), "Сервис выставил время создания с большой погрешностью"

    # Берем айди фильма который мы только что создали и  удаляем его из базы через апи
    # Удаляем фильм
    delete_response = super_admin.api.movies_api.delete_movie(movie_id=response["id"])
    assert delete_response.status_code == 200, "Фильм должен успешно удалиться"

    # проверяем что в конце тестирования фильма с таким названием действительно нет в базе
    movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name)
    assert movies_from_db.count() == 0, "Фильм небыл удален из базы!"

def test_delete_film(super_admin, db_session: Session):
    move_id=54

    movie_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.id == move_id)
    if movie_from_db.count() == 0:
        db_session.add(MovieDBModel(
        id = 54,
        name = "54ID",
        description = "Test54",
        price = 456,
        genre_id = 5,
        image_url = "gkkgkgkg",
        location = "MSK",
        rating = 3,
        published = False,
        created_at = datetime.datetime.now(),
            ))
        db_session.commit()

    delete_response = super_admin.api.movies_api.delete_movie(movie_id=move_id)
    assert delete_response.status_code == 200, "Film didn`t deleted"

    get_response = super_admin.api.movies_api.get_movies_by_id(movie_id=move_id, expected_status=404)
    assert get_response.status_code == 404, "Film didn`t deleted"

def test_accounts_transaction_template(db_session: Session):
        with allure.step("Создание тестовых данных в базе данных: счета Stan и Bob"):
            stan = AccountTransactionTemplate(user=f"Stan_{uuid.uuid4()}", balance=1000)
            bob = AccountTransactionTemplate(user=f"Bob_{uuid.uuid4()}", balance=500)
            db_session.add_all([stan, bob])
            db_session.commit()

        @allure.step("Функция перевода денег: transfer_money")
        @allure.description("""
            функция выполняющая транзакцию, имитация вызова функции на стороне тестируемого сервиса
            и вызывая метод transfer_money, мы как будто бы делаем запрос в api_manager.movies_api.transfer_money
            """)
        def transfer_money(session, from_account, to_account, amount):
            with allure.step(" Получаем счета"):
                from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
                to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

            with allure.step("Проверяем, что на счете достаточно средств"):
                if from_account.balance < amount:
                    raise ValueError("Недостаточно средств на счете")

            with allure.step("Выполняем перевод"):
                from_account.balance -= amount
                to_account.balance += amount

            with allure.step("Сохраняем изменения"):
                session.commit()

        # ====================================================================== Тест
        with allure.step("Проверяем начальные балансы"):
            assert stan.balance == 1000
            assert bob.balance == 500

        try:
            with allure.step("Выполняем перевод 200 единиц от stan к bob"):
                transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)

            with allure.step("Проверяем, что балансы изменились"):
                assert stan.balance == 800
                assert bob.balance == 700

        except Exception as e:
            with allure.step("ОШИБКА откаты транзакции"):
                db_session.rollback()

            pytest.fail(f"Ошибка при переводе денег: {e}")

        finally:
            with allure.step("Удаляем данные для тестирования из базы"):
                db_session.delete(stan)
                db_session.delete(bob)
                db_session.commit()