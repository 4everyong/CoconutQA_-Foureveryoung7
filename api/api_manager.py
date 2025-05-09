from api.movies_api import MoviesAPI


class ApiManager:
    def __init__(self, session):
        self.session = session
        self.movies_api = MoviesAPI(session)