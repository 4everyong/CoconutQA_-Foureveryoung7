from constants import BASE_URL
from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL)

    def get_movies(self):
        return self.send_request(
            method="GET",
            endpoint="/movies"
        )

    def get_movies_by_id(self, movie_id):
        return self.send_request(
            method="GET",
            endpoint=f"/movies?{movie_id}",

        )

    def get_movies_filter(self, movie_filter):
        return self.send_request(
            method="GET",
            endpoint=f"/movies?{movie_filter}"
        )

    def get_movies_by_id(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"/movies/{movie_id}",
            expected_status=expected_status
        )

    def create_movie(self, movie_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint="/movies",
            data=movie_data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id):
        return self.send_request(
            method="DELETE",
            endpoint=f"/movies/{movie_id}"
        )