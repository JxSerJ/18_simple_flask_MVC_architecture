# Здесь бизнес логика, в виде классов или методов. Сюда импортируются DAO классы из пакета dao и модели из dao.model.
# Некоторые методы могут оказаться просто прослойкой между dao и views,
# но чаще всего будет какая-то логика обработки данных сейчас или в будущем.

# Пример

# class BookService:
#
#     def __init__(self, book_dao: BookDAO):
#         self.book_dao = book_dao
#
#     def get_books(self) -> List["Book"]:
#         return self.book_dao.get_books()

from dao.movies import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.movie_dao = dao

    def get_movies_all(self):
        result = self.movie_dao.get_all()

        return result

    def get_movie_one(self, movie_id: int):
        result = self.movie_dao.get_one(movie_id)

        return result

    def create_movie(self, data):
        new_movie = self.movie_dao.create(data)

        return new_movie

    def update_movie(self, movie_id: int, data):
        result = self.movie_dao.update(movie_id, data)

        return result

    def update_movie_partial(self, movie_id: int, data):
        result = self.movie_dao.update_partial(movie_id, data)

        return result

    def delete_movie(self, movie_id: int):
        self.movie_dao.delete(movie_id)
