# Это файл для классов доступа к данным (Data Access Object). Здесь должен быть класс с методами доступа к данным.
# В методах можно построить сложные запросы к БД.


from dao.model.movies import Movie, MovieSchema

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


# CRUD
class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        query_data = self.session.query(Movie).all()
        return query_data

    def get_one(self, movie_id: int):
        query_data = self.session.query(Movie).get(movie_id)
        return query_data

    def create(self, data):
        new_movie = Movie(**data)

        self.session.add(new_movie)
        self.session.commit()
        return new_movie

    def update(self, movie_id: int, data):
        movie = self.get_one(movie_id)

        for k, v in data.items():
            setattr(movie, k, v)

        self.session.add(movie)
        self.session.commit()
        return movie

    def update_partial(self, movie_id: int, data):
        movie = self.get_one(movie_id)

        for k, v in data.items():
            setattr(movie, k, v)

        self.session.add(movie)
        self.session.commit()
        return movie

    def delete(self, movie_id: int):
        movie = self.get_one(movie_id)
        self.session.delete(movie)
        self.session.execute('VACUUM')
        self.session.commit()
