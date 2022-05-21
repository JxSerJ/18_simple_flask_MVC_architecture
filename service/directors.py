# Здесь бизнес логика, в виде классов или методов. Сюда импортируются DAO классы из пакета dao и модели из dao.model.
# Некоторые методы могут оказаться просто прослойкой между dao и views,
# но чаще всего будет какая-то логика обработки данных сейчас или в будущем.


from dao.directors import DirectorDAO
from dao.model.directors import Director, DirectorSchema
from service.validator import validator

director_schema = DirectorSchema()


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.director_dao = dao

    def get_all(self):
        result_data = self.director_dao.get_all()
        if not result_data:
            return f"Data not found. Empty database.", 404
        elif result_data == 500:
            return f"Database error", 500
        return result_data, 200

    def get_one(self, director_id: int):
        result_data = self.director_dao.get_one(director_id)
        if not result_data:
            return f"Data ID: {director_id} not found.", 404
        elif result_data == 500:
            return f"Database error", 500
        return result_data, 200

    def create(self, data):

        validation_result = validator("POST", data, Director, director_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]
        else:
            result_data = self.director_dao.create(data)
            if result_data == 500:
                return f"Database error", 500
            return result_data, 201

    def update(self, director_id: int, data):

        validation_result = validator("PUT", data, Director, director_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]
        else:
            director = self.get_one(director_id)
            if not director:
                return f"Data ID: {director_id} not found.", 404
            elif director[1] == 404:
                return director
            elif director == 500:
                return f"Database error", 500
            else:
                for k, v in data.items():
                    setattr(director[0], k, v)

                result = self.director_dao.update(director[0])
                if result == 500:
                    return f"Database error", 500
                return result, 200

    def update_partial(self, director_id: int, data):

        validation_result = validator("PATCH", data, Director, director_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]
        else:
            director = self.get_one(director_id)
            if not director:
                return f"Data ID: {director_id} not found.", 404
            elif director[1] == 404:
                return director
            elif director == 500:
                return f"Database error", 500
            else:
                for k, v in data.items():
                    setattr(director[0], k, v)

                result = self.director_dao.update(director[0])
                if result == 500:
                    return f"Database error", 500
                return result, 200

    def delete(self, director_id: int):

        query = self.get_one(director_id)
        if query[1] == 404:
            return f"Data ID: {director_id} not found.", 404
        elif query == 500:
            return f"Database error", 500
        else:
            result = self.director_dao.delete(director_id)
            if result == 500:
                return f"Database error", 500
            return f"Data ID: {director_id} was deleted successfully.", 200
