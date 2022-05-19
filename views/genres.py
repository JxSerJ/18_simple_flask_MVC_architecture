# Здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки).
# Сюда импортируются сервисы из пакета service.


from flask_restx import Resource, Namespace

genres_ns = Namespace('genres')


@genres_ns.route('/')
class MoviesView(Resource):

    def get(self):
        return "get_all", 200

    def post(self):
        return "post", 201


@genres_ns.route('/<int:genre_id>')
class MovieView(Resource):

    def get(self, genre_id: int):
        return "get_one", 200

    def put(self, genre_id: int):
        return "put", 200

    def patch(self, genre_id: int):
        return "patch", 200

    def delete(self, genre_id: int):
        return "delete", 200
