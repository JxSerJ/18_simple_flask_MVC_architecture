# Здесь бизнес логика, в виде классов или методов. Сюда импортируются DAO классы из пакета dao и модели из dao.model.
# Некоторые методы могут оказаться просто прослойкой между dao и views,
# но чаще всего будет какая-то логика обработки данных сейчас или в будущем.


from dao.movies import MovieDAO
from dao.model.movies import Movie, MovieSchema
from service.validator import validator

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.movie_dao = dao

    def get_all(self, director_id: int = None, genre_id: int = None, year: int = None):
        result_data = self.movie_dao.get_all(director_id=director_id, genre_id=genre_id, year=year)
        if not result_data:
            return f"Data not found. Empty database.", 404
        elif result_data == 500:
            return f"Database error", 500
        return result_data, 200

    def get_one(self, movie_id: int):
        result_data = self.movie_dao.get_one(movie_id)
        if not result_data:
            return f"Data ID: {movie_id} not found.", 404
        elif result_data == 500:
            return f"Database error", 500
        return result_data, 200

    def create(self, data):

        validation_result = validator("POST", data, Movie, movie_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]
        else:
            result_data = self.movie_dao.create(data)
            if result_data == 500:
                return f"Database error", 500
            return result_data, 201

    def update(self, movie_id: int, data):

        validation_result = validator("PUT", data, Movie, movie_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]
        else:
            movie = self.get_one(movie_id)
            if not movie:
                return f"Data ID: {movie_id} not found.", 404
            elif movie[1] == 404:
                return movie
            elif movie == 500:
                return f"Database error", 500
            else:
                for k, v in data.items():
                    setattr(movie[0], k, v)

                result = self.movie_dao.update(movie[0])
                if result == 500:
                    return f"Database error", 500
                return result, 200

    def update_partial(self, movie_id: int, data):

        validation_result = validator("PATCH", data, Movie, movie_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]
        else:
            movie = self.get_one(movie_id)
            if not movie:
                return f"Data ID: {movie_id} not found.", 404
            elif movie[1] == 404:
                return movie
            elif movie == 500:
                return f"Database error", 500
            else:
                for k, v in data.items():
                    setattr(movie[0], k, v)

                result = self.movie_dao.update(movie[0])
                if result == 500:
                    return f"Database error", 500
                return result, 200

    def delete(self, movie_id: int):

        query = self.get_one(movie_id)
        if query[1] == 404:
            return f"Data ID: {movie_id} not found.", 404
        elif query == 500:
            return f"Database error", 500
        else:
            result = self.movie_dao.delete(movie_id)
            if result == 500:
                return f"Database error", 500
            return f"Data ID: {movie_id} was deleted successfully.", 200
