# Это файл для классов доступа к данным (Data Access Object). Здесь должен быть класс с методами доступа к данным.
# В методах можно построить сложные запросы к БД.

from dao.model.movies import Movie, MovieSchema

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


# CRUD
class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self, director_id: int = None, genre_id: int = None, year: int = None):
        try:
            query = self.session.query(Movie)

            if director_id:
                query = query.filter(Movie.director_id == director_id)
            if genre_id:
                query = query.filter(Movie.genre_id == genre_id)
            if year:
                query = query.filter(Movie.year == year)

            result_data = query.all()
            return result_data

        except Exception:
            return 500

    def get_one(self, movie_id: int):
        try:
            query_data = self.session.query(Movie).get(movie_id)
            return query_data
        except Exception:
            return 500

    def create(self, data):
        try:
            new_movie = Movie(**data)

            self.session.add(new_movie)
            self.session.commit()
            return new_movie
        except Exception:
            return 500

    def update(self, movie):
        try:
            self.session.add(movie)
            self.session.commit()
            return movie
        except Exception as err:
            print(f'Database error: {err}')
            return 500

    def delete(self, movie_id: int):
        try:
            movie = self.get_one(movie_id)
            self.session.delete(movie)
            self.session.execute('VACUUM')
            self.session.commit()
        except Exception:
            return 500
