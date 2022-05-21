# Файл для создания DAO и сервисов доступа к ним отовсюду

from database.set_db import db

from dao.movies import MovieDAO
from dao.directors import DirectorDAO

from service.movies import MovieService
from service.directors import DirectorService


movie_dao = MovieDAO(db.session)
movie_service = MovieService(dao=movie_dao)

director_dao = DirectorDAO(db.session)
director_service = DirectorService(dao=director_dao)
#
# genre_dao = GenreDAO(db.session)
# genre_service = GenreService(dao=genre_dao)
