# Здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки).
# Сюда импортируются сервисы из пакета service.

from flask import request, jsonify
from flask_restx import Resource, Namespace

from container import genre_service
from dao.model.genres import GenreSchema


genres_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genres_ns.route('/')
class GenresView(Resource):

    def get(self):

        result_data = genre_service.get_all()

        if result_data[1] in [404, 500]:
            return result_data

        result = genres_schema.dump(result_data[0])
        return result, 200

    def post(self):
        request_data = request.json
        result_data = genre_service.create(request_data)

        if result_data[1] in [422, 500, 400]:
            return result_data

        result = genre_schema.dump(result_data[0])
        data_id = result["id"]
        response = jsonify(result)
        response.status_code = 201
        response.headers['location'] = f'/{genres_ns.name}/{data_id}'
        return response


@genres_ns.route('/<int:genre_id>')
class GenreView(Resource):

    def get(self, genre_id: int):
        result_data = genre_service.get_one(genre_id)

        if result_data[1] in [404, 500]:
            return result_data

        result = genre_schema.dump(result_data[0])
        return result, 200

    def put(self, genre_id: int):
        request_data = request.json
        result_data = genre_service.update(genre_id, request_data)

        if result_data[1] in [404, 500, 422]:
            return result_data

        result = genre_schema.dump(result_data[0])
        return result, 200

    def patch(self, genre_id: int):
        request_data = request.json
        result_data = genre_service.update_partial(genre_id, request_data)

        if result_data[1] in [500, 422, 404]:
            return result_data

        result = genre_schema.dump(result_data[0])
        return result, 200

    def delete(self, genre_id: int):
        result_data = genre_service.delete(genre_id)
        return result_data
