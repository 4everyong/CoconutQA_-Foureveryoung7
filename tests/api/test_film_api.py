from tests.api.conftest import data_film, data_film_min

class TestMoviesAPI:
    def test_get_films(self, api_manager):
        response = api_manager.movies_api.get_movies()
        assert isinstance(response.json()["movies"], list)

    def test_get_films_by_filter(self, api_manager, movie_filter="locations=MSK&locations=SPB&published=true&genreId=1"):
        response = api_manager.movies_api.get_movies_filter(movie_filter=movie_filter)
        data_filter = response.json()
        for i in range(len(data_filter["movies"])):
            assert data_filter["movies"][i]["genreId"] == 1, "genreId is not 1"
            assert data_filter["movies"][i]["published"] == True, "published is not True"
            assert data_filter["movies"][i]["location"] == "MSK" or "SPB", "location is not MSK or SPB"

    def test_get_film_by_id(self, api_manager, data_film):
        response = api_manager.movies_api.create_movie(movie_data=data_film)
        data_film = response.json()
        id_film = data_film.get("id")
        get_film = api_manager.movies_api.get_movies_by_id(movie_id=id_film, expected_status=200)
        data_get_film = get_film.json()
        assert "id" in data_get_film
        assert "id" in data_film, "id is not in data_film"
        assert data_film["name"] == "Тестовый фильм", "name is not Тестовый фильм"
        assert data_film["price"] == 1240, "price is not 1240"
        assert data_film["location"] == "MSK", "location is not MSK"
        assert data_film["description"] == "Тестовое описание", "description is not Тестовое описание"
        assert data_film["genreId"] == 1, "genreId is not 1"
        delete_film = api_manager.movies_api.delete_movie(id_film)

    def test_post_and_delete_film(self, api_manager, data_film):
        response = api_manager.movies_api.create_movie(movie_data=data_film)
        data_film = response.json()
        id_film = data_film.get("id")
        assert "id" in data_film, "id is not in data_film"
        assert data_film["name"] == "Тестовый фильм", "name is not Тестовый фильм"
        assert data_film["price"] == 1240, "price is not 1240"
        assert data_film["location"] == "MSK", "location is not MSK"
        assert data_film["description"] == "Тестовое описание", "description is not Тестовое описание"
        assert data_film["genreId"] == 1, "genreId is not 1"
        assert data_film["imageUrl"] == "https://image.url", "imageUrl is not correct"
        response = api_manager.movies_api.delete_movie(id_film)
        get_film = api_manager.movies_api.get_movies_by_id(movie_id=id_film,expected_status=404)

    def test_negative_double_post(self, api_manager, data_film):
        response1 = api_manager.movies_api.create_movie(movie_data=data_film)
        response2 = api_manager.movies_api.create_movie(movie_data=data_film, expected_status=409)
        assert response2.status_code == 409, "status_code is not 409"
        id_film = response1.json().get("id")
        api_manager.movies_api.delete_movie(id_film)
        api_manager.movies_api.get_movies_by_id(movie_id=id_film, expected_status=404)

    def test_negative_min_post(self, api_manager, data_film_min):
        response = api_manager.movies_api.create_movie(movie_data=data_film_min)
        assert data_film_min["name"] == "Тестовый фильм", "name is not Тестовый фильм"
        assert data_film_min["price"] == 1240, "price is not 1240"
        assert data_film_min["location"] == "MSK", "location is not MSK"
        assert data_film_min["description"] == "Тестовое описание", "description is not Тестовое описание"
        assert data_film_min["genreId"] == 1, "genreId is not 1"
        assert "imageUrl" not in data_film_min, "imageUrl присутствует, а должен отсутствовать"
        id_film = response.json().get("id")
        response = api_manager.movies_api.delete_movie(id_film)
        get_film = api_manager.movies_api.get_movies_by_id(movie_id=id_film, expected_status=404)




