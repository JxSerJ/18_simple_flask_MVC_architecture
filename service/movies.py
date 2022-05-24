# Здесь бизнес логика, в виде классов или методов. Сюда импортируются DAO классы из пакета dao и модели из dao.model.
# Некоторые методы могут оказаться просто прослойкой между dao и views,
# но чаще всего будет какая-то логика обработки данных сейчас или в будущем.


from dao.movies import MovieDAO
from dao.model.movies import Movie, MovieSchema
from service.validator import validator

movie_schema = MovieSchema()


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.movie_dao = dao

    def get_all(self, director_id: int = None, genre_id: int = None, year: int = None):
        result_data = self.movie_dao.get_all(director_id=director_id, genre_id=genre_id, year=year)
        if not result_data:
            return {"result": f"Data not found. Empty database.", "status_code": 404}
        return {"result": result_data, "status_code": 200}

    def get_one(self, movie_id: int):
        result_data = self.movie_dao.get_one(movie_id)
        if not result_data:
            return {"result": f"Data ID: {movie_id} not found.", "status_code": 404}
        return {"result": result_data, "status_code": 200}

    def create(self, data):

        validation_result = validator("POST", data, Movie, movie_schema)
        if validation_result['is_error']:
            return {"result": validation_result["error_message"], "status_code": validation_result["status_code"]}
        else:
            result_data = self.movie_dao.create(data)
            return {"result": result_data, "status_code": 201}

    def update(self, movie_id: int, data):

        movie = self.movie_dao.get_one(movie_id)
        result_data = self.movie_dao.update(movie, data)
        return {"result": result_data, "status_code": 200}

    def update_partial(self, movie_id: int, data):

        movie = self.movie_dao.get_one(movie_id)
        result_data = self.movie_dao.update(movie, data)
        return {"result": result_data, "status_code": 200}

    def delete(self, movie_id: int):

        query = self.movie_dao.get_one(movie_id)
        if not query:
            return {"result": f"Data ID: {movie_id} not found.", "status_code": 404}
        else:
            self.movie_dao.delete(movie_id)
            return {"result": f"Data ID: {movie_id} was deleted successfully.", "status_code": 200}
