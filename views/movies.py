# Здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки).
# Сюда импортируются сервисы из пакета service.

from flask import request, jsonify
from flask_restx import Resource, Namespace
from marshmallow import ValidationError

from container import movie_service
from dao.model.movies import MovieSchema


movies_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route('/')
class MoviesView(Resource):

    def get(self):

        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        year = request.args.get('year')

        result_data = movie_service.get_all(director_id=director_id, genre_id=genre_id, year=year)

        if result_data["status_code"] in [404, 500]:
            return result_data["result"], result_data["status_code"]

        result = movies_schema.dump(result_data["result"])
        return result, result_data["status_code"]

    def post(self):

        request_data = request.json
        result_data = movie_service.create(request_data)

        if result_data["status_code"] in [422, 500, 400]:
            return result_data["result"], result_data["status_code"]

        result = movie_schema.dump(result_data["result"])

        data_id = result["id"]

        response = jsonify(result)
        response.status_code = result_data["status_code"]
        response.headers['location'] = f'/{movies_ns.name}/{data_id}'

        return response


@movies_ns.route('/<int:mov_id>')
class MovieView(Resource):

    def get(self, mov_id: int):

        result_data = movie_service.get_one(mov_id)

        if result_data["status_code"] in [422, 404]:
            return result_data["result"], result_data["status_code"]

        result = movie_schema.dump(result_data["result"])
        return result, result_data["status_code"]

    def put(self, mov_id: int):

        request_data = request.json
        try:
            request_data = movie_schema.load(request_data)
        except ValidationError as err:
            return f"{err}", 400

        result_data = movie_service.update(mov_id, request_data)

        if result_data["status_code"] in [422, 404]:
            return result_data["result"], result_data["status_code"]

        result = movie_schema.dump(result_data["result"])
        return result, result_data["status_code"]

    def patch(self, mov_id: int):

        request_data = request.json
        try:
            request_data = movie_schema.load(request_data)
        except ValidationError as err:
            return f"{err}", 400

        result_data = movie_service.update_partial(mov_id, request_data)

        if result_data["status_code"] in [422, 404]:
            return result_data["result"], result_data["status_code"]

        result = movie_schema.dump(result_data["result"])
        return result, result_data["status_code"]

    def delete(self, mov_id: int):

        result_data = movie_service.delete(mov_id)
        return result_data["result"], result_data["status_code"]
