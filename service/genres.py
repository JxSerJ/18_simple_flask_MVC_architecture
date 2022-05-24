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
            return {"result": f"Data not found. Empty database.", "status_code": 404}
        return {"result": result_data, "status_code": 200}

    def get_one(self, genre_id: int):
        result_data = self.genre_dao.get_one(genre_id)
        if not result_data:
            return {"result": f"Data ID: {genre_id} not found.", "status_code": 404}
        return {"result": result_data, "status_code": 200}

    def create(self, data):

        validation_result = validator("POST", data, Genre, genre_schema)
        if validation_result['is_error']:
            return {"result": validation_result["error_message"], "status_code": validation_result["status_code"]}
        else:
            result_data = self.genre_dao.create(data)
            return {"result": result_data, "status_code": 201}

    def update(self, genre_id: int, data):

        genre = self.genre_dao.get_one(genre_id)
        result_data = self.genre_dao.update(genre, data)
        return {"result": result_data, "status_code": 200}

    def update_partial(self, genre_id: int, data):

        genre = self.genre_dao.get_one(genre_id)
        result_data = self.genre_dao.update(genre, data)
        return {"result": result_data, "status_code": 200}

    def delete(self, genre_id: int):

        query = self.genre_dao.get_one(genre_id)
        if not query:
            return {"result": f"Data ID: {genre_id} not found.", "status_code": 404}
        else:
            self.genre_dao.delete(genre_id)
            return {"result": f"Data ID: {genre_id} was deleted successfully.", "status_code": 200}
