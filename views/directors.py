# Здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки).
# Сюда импортируются сервисы из пакета service.

from flask import request, jsonify
from flask_restx import Resource, Namespace

from container import director_service
from dao.model.directors import DirectorSchema


directors_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@directors_ns.route('/')
class DirectorsView(Resource):

    def get(self):

        result_data = director_service.get_all()

        if result_data[1] in [404, 500]:
            return result_data

        result = directors_schema.dump(result_data[0])
        return result, 200

    def post(self):
        request_data = request.json
        result_data = director_service.create(request_data)

        if result_data[1] in [422, 500, 400]:
            return result_data

        result = director_schema.dump(result_data[0])
        data_id = result["id"]
        response = jsonify(result)
        response.status_code = 201
        response.headers['location'] = f'/{directors_ns.name}/{data_id}'
        return response


@directors_ns.route('/<int:dir_id>')
class DirectorView(Resource):

    def get(self, dir_id: int):
        result_data = director_service.get_one(dir_id)

        if result_data[1] in [404, 500]:
            return result_data

        result = director_schema.dump(result_data[0])
        return result, 200

    def put(self, dir_id: int):
        request_data = request.json
        result_data = director_service.update(dir_id, request_data)

        if result_data[1] in [404, 500, 422]:
            return result_data

        result = director_schema.dump(result_data[0])
        return result, 200

    def patch(self, dir_id: int):
        request_data = request.json
        result_data = director_service.update_partial(dir_id, request_data)

        if result_data[1] in [500, 422, 404]:
            return result_data

        result = director_schema.dump(result_data[0])
        return result, 200

    def delete(self, dir_id: int):
        result_data = director_service.delete(dir_id)
        return result_data
