# Здесь бизнес логика, в виде классов или методов. Сюда импортируются DAO классы из пакета dao и модели из dao.model.
# Некоторые методы могут оказаться просто прослойкой между dao и views,
# но чаще всего будет какая-то логика обработки данных сейчас или в будущем.


from dao.genres import GenreDAO
from dao.model.genres import Genre, GenreSchema
from service.validator import validator

genre_schema = GenreSchema()


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.genre_dao = dao

    def get_all(self):
        result_data = self.genre_dao.get_all()
        if not result_data:
            return f"Data not found. Empty database.", 404
        elif result_data == 500:
            return f"Database error", 500
        return result_data, 200

    def get_one(self, genre_id: int):
        result_data = self.genre_dao.get_one(genre_id)
        if not result_data:
            return f"Data ID: {genre_id} not found.", 404
        elif result_data == 500:
            return f"Database error", 500
        return result_data, 200

    def create(self, data):

        validation_result = validator("POST", data, Genre, genre_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]
        else:
            result_data = self.genre_dao.create(data)
            if result_data == 500:
                return f"Database error", 500
            return result_data, 201

    def update(self, genre_id: int, data):

        validation_result = validator("PUT", data, Genre, genre_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]
        else:
            genre = self.get_one(genre_id)
            if not genre:
                return f"Data ID: {genre_id} not found.", 404
            elif genre[1] == 404:
                return genre
            elif genre == 500:
                return f"Database error", 500
            else:
                for k, v in data.items():
                    setattr(genre[0], k, v)

                result = self.genre_dao.update(genre[0])
                if result == 500:
                    return f"Database error", 500
                return result, 200

    def update_partial(self, genre_id: int, data):

        validation_result = validator("PATCH", data, Genre, genre_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]
        else:
            genre = self.get_one(genre_id)
            if not genre:
                return f"Data ID: {genre_id} not found.", 404
            elif genre[1] == 404:
                return genre
            elif genre == 500:
                return f"Database error", 500
            else:
                for k, v in data.items():
                    setattr(genre[0], k, v)

                result = self.genre_dao.update(genre[0])
                if result == 500:
                    return f"Database error", 500
                return result, 200

    def delete(self, genre_id: int):

        query = self.get_one(genre_id)
        if query[1] == 404:
            return f"Data ID: {genre_id} not found.", 404
        elif query == 500:
            return f"Database error", 500
        else:
            result = self.genre_dao.delete(genre_id)
            if result == 500:
                return f"Database error", 500
            return f"Data ID: {genre_id} was deleted successfully.", 200
