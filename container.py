# Файл для создания DAO и сервисов доступа к ним отовсюду

# book_dao = BookDAO(db.session)
# book_service = BookService(dao=book_dao)
#
# review_dao = ReviewDAO(db.session)
# review_service = ReviewService(dao=review_dao)

from database.set_db import db

from dao.movies import MovieDAO

from service.movies import MovieService


movie_dao = MovieDAO(db.session)
movie_service = MovieService(dao=movie_dao)

# director_dao = DirectorDAO(db.session)
# director_service = DirectorService(dao=director_dao)
#
# genre_dao = GenreDAO(db.session)
# genre_service = GenreService(dao=genre_dao)
