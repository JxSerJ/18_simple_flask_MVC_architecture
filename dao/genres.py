# Это файл для классов доступа к данным (Data Access Object). Здесь должен быть класс с методами доступа к данным.
# В методах можно построить сложные запросы к БД.

from dao.model.genres import Genre


# CRUD
class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        try:
            result_data = self.session.query(Genre).all()
            return result_data

        except Exception as err:
            print(f'Database error: {err}')
            return 500

    def get_one(self, genre_id: int):
        try:
            query_data = self.session.query(Genre).get(genre_id)
            return query_data

        except Exception as err:
            print(f'Database error: {err}')
            return 500

    def create(self, data):
        try:
            new_genre = Genre(**data)

            self.session.add(new_genre)
            self.session.commit()
            return new_genre

        except Exception as err:
            print(f'Database error: {err}')
            return 500

    def update(self, genre):
        try:
            self.session.add(genre)
            self.session.commit()
            return genre

        except Exception as err:
            print(f'Database error: {err}')
            return 500

    def delete(self, genre_id: int):
        try:
            genre = self.get_one(genre_id)
            self.session.delete(genre)
            self.session.execute('VACUUM')
            self.session.commit()

        except Exception as err:
            print(f'Database error: {err}')
            return 500
