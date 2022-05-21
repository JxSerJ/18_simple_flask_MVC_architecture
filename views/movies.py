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

        result_data = movie_service.get_movies_all(director_id=director_id, genre_id=genre_id, year=year)
        result = movies_schema.dump(result_data)
        return result, 200

    def post(self):
        request_data = request.json
        new_movie = movie_service.create_movie(request_data)
        result = movie_schema.dump(new_movie)
        return result, 201


@movies_ns.route('/<int:mov_id>')
class MovieView(Resource):

    def get(self, mov_id: int):
        result_data = movie_service.get_movie_one(mov_id)
        result = movie_schema.dump(result_data)
        return result, 200

    def put(self, mov_id: int):
        request_data = request.json
        result_data = movie_service.update_movie(mov_id, request_data)
        result = movie_schema.dump(result_data)
        return result, 200

    def patch(self, mov_id: int):
        request_data = request.json
        result_data = movie_service.update_movie_partial(mov_id, request_data)
        result = movie_schema.dump(result_data)
        return result, 200

    def delete(self, mov_id: int):
        movie_service.delete_movie(mov_id)
        return f"Data ID: {mov_id} was deleted successfully.", 200
