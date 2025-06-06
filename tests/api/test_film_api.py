import allure
import pytest
from conftest import data_film, data_film_min, create_delete_film, super_admin
from db_requester.models import MovieDBModel
from models.base_models import FilmRequest, FilmResponse

@allure.epic("Тестирование API")
@allure.mark.api
class TestMoviesAPI:
    test_data = [
        (1, 100, ['MSK'], 1),
        (100, 10000, ['SPB'], 2),
        (1, 1000, ['MSK', 'SPB'], 3)
    ]

    @allure.title("Получения фильмов по параметрам")
    @pytest.mark.parametrize('minPrice,maxPrice,locations,genreId', test_data)
    def test_get_films(self, super_admin, minPrice, maxPrice, locations, genreId):
        params = {
            'pageSize': 10,
            'page': 10,
            'minPrice': minPrice,
            'maxPrice': maxPrice,
            'locations': locations,
            'published': True,
            'genreId': genreId
        }
        response = super_admin.api.movies_api.get_movies(params=params)
        assert isinstance(response.json()["movies"], list)

    def test_get_films_by_filter(self, super_admin,
                                 movie_filter="locations=MSK&locations=SPB&published=true&genreId=1"):
        response = super_admin.api.movies_api.get_movies_filter(movie_filter=movie_filter)
        data_filter = response.json()
        for i in range(len(data_filter["movies"])):
            assert data_filter["movies"][i]["genreId"] == 1, "genreId is not 1"
            assert data_filter["movies"][i]["published"] == True, "published is not True"
            assert data_filter["movies"][i]["location"] == "MSK" or "SPB", "location is not MSK or SPB"

    def test_get_film_by_id(self, create_delete_film: FilmRequest, super_admin):
        id_film = create_delete_film.id
        get_film = super_admin.api.movies_api.get_movies_by_id(movie_id=id_film, expected_status=200)
        film_data = FilmRequest(**get_film.json())
        assert film_data.name == create_delete_film.name, "name не совпадает"
        assert film_data.price == create_delete_film.price, "price не совпадает"
        assert film_data.location == create_delete_film.location, "location не совпадает"
        assert film_data.description == create_delete_film.description, "description не совпадает"
        assert film_data.genreId == create_delete_film.genreId, "genreId не совпадает"

    def test_post_film(self, data_film, create_delete_film):
        assert create_delete_film.name == data_film.name, "name не совпадает"
        assert create_delete_film.price == data_film.price, "price не совпадает"
        assert create_delete_film.location == data_film.location, "location не совпадает"
        assert create_delete_film.description == data_film.description, "description не совпадает"
        assert create_delete_film.genreId == data_film.genreId, "genreId не совпадает"
        assert create_delete_film.imageUrl == data_film.imageUrl, "imageUrl не совпадает"

    def test_delete_film(self, create_film, super_admin):
        id_film = create_film.id
        super_admin.api.movies_api.delete_movie(id_film)
        super_admin.api.movies_api.get_movies_by_id(id_film, expected_status=404)

    def test_negative_double_post(self, data_film, super_admin):
        response1 = super_admin.api.movies_api.create_movie(movie_data=data_film)
        super_admin.api.movies_api.create_movie(movie_data=data_film, expected_status=409)
        id_film = response1.json().get("id")
        super_admin.api.movies_api.delete_movie(id_film)
        super_admin.api.movies_api.get_movies_by_id(movie_id=id_film, expected_status=404)

    def test_negative_min_post(self, data_film_min, super_admin, db_session):
        response_data = super_admin.api.movies_api.create_movie(movie_data=data_film_min).json()
        response_data = FilmResponse(**response_data)
        id_film = response_data.id
        movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.id == id_film)
        assert movies_from_db.count() == 1
        assert data_film_min.name == response_data.name, "name не совпадает"
        assert data_film_min.price == response_data.price, "price не совпадает"
        assert data_film_min.location == response_data.location, "location не совпадает"
        assert data_film_min.description == response_data.description, "description не совпадает"
        assert data_film_min.genreId == response_data.genreId, "genreId не совпадает"
        assert "imageUrl" not in data_film_min, "imageUrl присутствует, а должен отсутствовать"
        super_admin.api.movies_api.delete_movie(id_film)
        super_admin.api.movies_api.get_movies_by_id(movie_id=id_film, expected_status=404)