# Основной файл приложения. Здесь конфигурируется фласк, сервисы, SQLAlchemy и всё остальное,
# что требуется для приложения.

# Этот файл часто является точкой входа в приложение.


from flask import Flask

from set_db import db
from set_api import api
from database.create_db import create_data

from views.movies import movies_ns
from views.directors import directors_ns
from views.genres import genres_ns

from config import Config


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    initialize_extensions(app)
    return app


def initialize_extensions(app):
    db.init_app(app)
    api.init_app(app)
    api.add_namespace(movies_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)
    with app.app_context():
        create_data(db)


application = create_app(Config)

if __name__ == '__main__':
    application.run(host='localhost', port=5000)