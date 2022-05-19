# Здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки).
# Сюда импортируются сервисы из пакета service.


from flask_restx import Resource, Namespace

directors_ns = Namespace('directors')


@directors_ns.route('/')
class DirectorsView(Resource):

    def get(self):
        return "get_all", 200

    def post(self):
        return "post", 201


@directors_ns.route('/<int:dir_id>')
class DirectorView(Resource):

    def get(self, dir_id: int):
        return "get_one", 200

    def put(self, dir_id: int):
        return "put", 200

    def patch(self, dir_id: int):
        return "patch", 200

    def delete(self, dir_id: int):
        return "delete", 200
