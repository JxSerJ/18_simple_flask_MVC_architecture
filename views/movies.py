# Здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки).
# Сюда импортируются сервисы из пакета service.

from flask import request
from flask_restx import Resource, Namespace

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

        if result_data[1] in [404, 500]:
            return result_data

        result = movies_schema.dump(result_data[0])
        return result, 200

    def post(self):
        request_data = request.json
        result_data = movie_service.create(request_data)

        if result_data[1] in [422, 500, 400]:
            return result_data

        result = movie_schema.dump(result_data[0])
        return result, 200


@movies_ns.route('/<int:mov_id>')
class MovieView(Resource):

    def get(self, mov_id: int):
        result_data = movie_service.get_one(mov_id)

        if result_data[1] in [404, 500]:
            return result_data

        result = movie_schema.dump(result_data[0])
        return result, 200

    def put(self, mov_id: int):
        request_data = request.json
        result_data = movie_service.update(mov_id, request_data)

        if result_data[1] in [404, 500, 422]:
            return result_data

        result = movie_schema.dump(result_data[0])
        return result, 200

    def patch(self, mov_id: int):
        request_data = request.json
        result_data = movie_service.update_partial(mov_id, request_data)

        if result_data[1] in [500, 422, 404]:
            return result_data

        result = movie_schema.dump(result_data[0])
        return result, 200

    def delete(self, mov_id: int):
        result_data = movie_service.delete(mov_id)
        return result_data
