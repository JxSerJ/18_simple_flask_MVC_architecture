# Это файл для классов доступа к данным (Data Access Object). Здесь должен быть класс с методами доступа к данным.
# В методах можно построить сложные запросы к БД.

from dao.model.directors import Director, DirectorSchema


# CRUD
class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        try:
            result_data = self.session.query(Director).all()
            return result_data

        except Exception as err:
            print(f'Database error: {err}')
            return 500

    def get_one(self, director_id: int):
        try:
            query_data = self.session.query(Director).get(director_id)
            return query_data

        except Exception as err:
            print(f'Database error: {err}')
            return 500

    def create(self, data):
        try:
            new_director = Director(**data)

            self.session.add(new_director)
            self.session.commit()
            return new_director

        except Exception as err:
            print(f'Database error: {err}')
            return 500

    def update(self, director):
        try:
            self.session.add(director)
            self.session.commit()
            return director

        except Exception as err:
            print(f'Database error: {err}')
            return 500

    def delete(self, director_id: int):
        try:
            director = self.get_one(director_id)
            self.session.delete(director)
            self.session.execute('VACUUM')
            self.session.commit()

        except Exception as err:
            print(f'Database error: {err}')
            return 500
