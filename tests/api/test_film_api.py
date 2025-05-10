from tests.api.conftest import data_film, data_film_min, create_delete_film


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

    def test_get_film_by_id(self, api_manager, create_delete_film):
        id_film = create_delete_film.get("id")
        get_film = api_manager.movies_api.get_movies_by_id(movie_id=id_film, expected_status=200).json()
        assert "id" in create_delete_film
        assert get_film["name"] == create_delete_film["name"], "name не совпадает"
        assert get_film["price"] == create_delete_film["price"], "price не совпадает"
        assert get_film["location"] == create_delete_film["location"], "location не совпадает"
        assert get_film["description"] == create_delete_film["description"], "description не совпадает"
        assert get_film["genreId"] == create_delete_film["genreId"], "genreId не совпадает"

    def test_post_film(self, api_manager, data_film, create_delete_film):
        assert "id" in create_delete_film, "id is not in data_film"
        assert create_delete_film["name"] == data_film["name"], "name не совпадает"
        assert create_delete_film["price"] == data_film["price"], "price не совпадает"
        assert create_delete_film["location"] == data_film["location"], "location не совпадает"
        assert create_delete_film["description"] == data_film["description"], "description не совпадает"
        assert create_delete_film["genreId"] == data_film["genreId"], "genreId не совпадает"
        assert create_delete_film["imageUrl"] == data_film["imageUrl"], "imageUrl не совпадает"

    def test_delete_film(self, create_film, api_manager):
        id_film = create_film.get("id")
        api_manager.movies_api.delete_movie(id_film)
        api_manager.movies_api.get_movies_by_id(id_film, expected_status=404)

    def test_negative_double_post(self, api_manager, data_film):
        response1 = api_manager.movies_api.create_movie(movie_data=data_film)
        api_manager.movies_api.create_movie(movie_data=data_film, expected_status=409)
        id_film = response1.json().get("id")
        api_manager.movies_api.delete_movie(id_film)
        api_manager.movies_api.get_movies_by_id(movie_id=id_film, expected_status=404)

    def test_negative_min_post(self, api_manager, data_film_min):
        response_data = api_manager.movies_api.create_movie(movie_data=data_film_min).json()
        id_film = response_data.get("id")
        assert data_film_min["name"] == response_data["name"], "name не совпадает"
        assert data_film_min["price"] == response_data["price"], "price не совпадает"
        assert data_film_min["location"] == response_data["location"], "location не совпадает"
        assert data_film_min["description"] == response_data["description"], "description не совпадает"
        assert data_film_min["genreId"] == response_data["genreId"], "genreId не совпадает"
        assert "imageUrl" not in data_film_min, "imageUrl присутствует, а должен отсутствовать"
        api_manager.movies_api.delete_movie(id_film)
        api_manager.movies_api.get_movies_by_id(movie_id=id_film, expected_status=404)




