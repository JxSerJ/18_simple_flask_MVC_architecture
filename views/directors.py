# Здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки).
# Сюда импортируются сервисы из пакета service.

from flask import request, jsonify
from flask_restx import Resource, Namespace
from marshmallow import ValidationError

from container import director_service
from dao.model.directors import DirectorSchema


directors_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@directors_ns.route('/')
class DirectorsView(Resource):

    def get(self):

        result_data = director_service.get_all()

        if result_data["status_code"] in [404, 500]:
            return result_data["result"], result_data["status_code"]

        result = directors_schema.dump(result_data["result"])
        return result, result_data["status_code"]

    def post(self):

        request_data = request.json
        result_data = director_service.create(request_data)

        if result_data["status_code"] in [422, 500, 400]:
            return result_data["result"], result_data["status_code"]

        result = director_schema.dump(result_data["result"])

        data_id = result["id"]

        response = jsonify(result)
        response.status_code = result_data["status_code"]
        response.headers['location'] = f'/{directors_ns.name}/{data_id}'

        return response


@directors_ns.route('/<int:director_id>')
class DirectorView(Resource):

    def get(self, director_id: int):

        result_data = director_service.get_one(director_id)

        if result_data["status_code"] in [422, 404]:
            return result_data["result"], result_data["status_code"]

        result = director_schema.dump(result_data["result"])
        return result, result_data["status_code"]

    def put(self, director_id: int):

        request_data = request.json
        try:
            request_data = director_schema.load(request_data)
        except ValidationError as err:
            return f"{err}", 400
        # check if all keys acquired
        schema_keys = set(director_schema.fields.keys())
        schema_keys.remove('id')
        data_keys = request_data.keys()
        if 'id' in data_keys:
            data_keys = set(data_keys.remove('id'))
        else:
            data_keys = set(data_keys)
        if data_keys != schema_keys:
            return "Not all keys acquired", 400

        result_data = director_service.update(director_id, request_data)

        if result_data["status_code"] in [422, 404]:
            return result_data["result"], result_data["status_code"]

        result = director_schema.dump(result_data["result"])
        return result, result_data["status_code"]

    def patch(self, director_id: int):

        request_data = request.json
        try:
            request_data = director_schema.load(request_data)
        except ValidationError as err:
            return f"{err}", 400

        result_data = director_service.update_partial(director_id, request_data)

        if result_data["status_code"] in [422, 404]:
            return result_data["result"], result_data["status_code"]

        result = director_schema.dump(result_data["result"])
        return result, result_data["status_code"]

    def delete(self, director_id: int):

        result_data = director_service.delete(director_id)
        return result_data["result"], result_data["status_code"]
