# Здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки).
# Сюда импортируются сервисы из пакета service.


from flask_restx import Resource, Namespace

movies_ns = Namespace('movies')


@movies_ns.route('/')
class MoviesView(Resource):

    def get(self):
        return "get_all", 200

    def post(self):
        return "post", 201


@movies_ns.route('/<int:mov_id>')
class MovieView(Resource):

    def get(self, mov_id: int):
        return "get_one", 200

    def put(self, mov_id: int):
        return "put", 200

    def patch(self, mov_id: int):
        return "patch", 200

    def delete(self, mov_id: int):
        return "delete", 200
