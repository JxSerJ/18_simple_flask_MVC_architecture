# Здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки).
# Сюда импортируются сервисы из пакета service.

from flask import request, jsonify
from flask_restx import Resource, Namespace
from marshmallow import ValidationError

from container import genre_service
from dao.model.genres import GenreSchema


genres_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genres_ns.route('/')
class GenresView(Resource):

    def get(self):

        result_data = genre_service.get_all()

        if result_data["status_code"] in [404, 500]:
            return result_data["result"], result_data["status_code"]

        result = genres_schema.dump(result_data["result"])
        return result, result_data["status_code"]

    def post(self):

        request_data = request.json
        result_data = genre_service.create(request_data)

        if result_data["status_code"] in [422, 500, 400]:
            return result_data["result"], result_data["status_code"]

        result = genre_schema.dump(result_data["result"])

        data_id = result["id"]

        response = jsonify(result)
        response.status_code = result_data["status_code"]
        response.headers['location'] = f'/{genres_ns.name}/{data_id}'

        return response


@genres_ns.route('/<int:genre_id>')
class GenreView(Resource):

    def get(self, genre_id: int):

        result_data = genre_service.get_one(genre_id)

        if result_data["status_code"] in [422, 404]:
            return result_data["result"], result_data["status_code"]

        result = genre_schema.dump(result_data["result"])
        return result, result_data["status_code"]

    def put(self, genre_id: int):

        request_data = request.json
        try:
            request_data = genre_schema.load(request_data)
        except ValidationError as err:
            return f"{err}", 400
        # check if all keys acquired
        schema_keys = set(genre_schema.fields.keys())
        schema_keys.remove('id')
        data_keys = request_data.keys()
        if 'id' in data_keys:
            data_keys = set(data_keys.remove('id'))
        else:
            data_keys = set(data_keys)
        if data_keys != schema_keys:
            return "Not all keys acquired", 400

        result_data = genre_service.update(genre_id, request_data)

        if result_data["status_code"] in [422, 404]:
            return result_data["result"], result_data["status_code"]

        result = genre_schema.dump(result_data["result"])
        return result, result_data["status_code"]

    def patch(self, genre_id: int):

        request_data = request.json
        try:
            request_data = genre_schema.load(request_data)
        except ValidationError as err:
            return f"{err}", 400

        result_data = genre_service.update_partial(genre_id, request_data)

        if result_data["status_code"] in [422, 404]:
            return result_data["result"], result_data["status_code"]

        result = genre_schema.dump(result_data["result"])
        return result, result_data["status_code"]

    def delete(self, genre_id: int):

        result_data = genre_service.delete(genre_id)
        return result_data["result"], result_data["status_code"]
