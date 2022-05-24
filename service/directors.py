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
            return {"result": f"Data not found. Empty database.", "status_code": 404}
        return {"result": result_data, "status_code": 200}

    def get_one(self, director_id: int):
        result_data = self.director_dao.get_one(director_id)
        if not result_data:
            return {"result": f"Data ID: {director_id} not found.", "status_code": 404}
        return {"result": result_data, "status_code": 200}

    def create(self, data):

        validation_result = validator("POST", data, Director, director_schema)
        if validation_result['is_error']:
            return {"result": validation_result["error_message"], "status_code": validation_result["status_code"]}
        else:
            result_data = self.director_dao.create(data)
            return {"result": result_data, "status_code": 201}

    def update(self, director_id: int, data):

        director = self.director_dao.get_one(director_id)
        result_data = self.director_dao.update(director, data)
        return {"result": result_data, "status_code": 200}

    def update_partial(self, director_id: int, data):

        director = self.director_dao.get_one(director_id)
        result_data = self.director_dao.update(director, data)
        return {"result": result_data, "status_code": 200}

    def delete(self, director_id: int):

        query = self.director_dao.get_one(director_id)
        if not query:
            return {"result": f"Data ID: {director_id} not found.", "status_code": 404}
        else:
            self.director_dao.delete(director_id)
            return {"result": f"Data ID: {director_id} was deleted successfully.", "status_code": 200}
