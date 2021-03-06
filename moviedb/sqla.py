from . import db
import sqlalchemy as sqla
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker,relationship

Base = declarative_base()

GenreInFilm=sqla.Table(
    'genre_in_film',Base.metadata,
    sqla.Column('film_id',sqla.String,sqla.ForeignKey('films.title')),
    sqla.Column('genre_id',sqla.String,sqla.ForeignKey('genres.title')),
    )


class FilmInDB(Base):

    __tablename__ = 'films'

    title = sqla.Column(sqla.String, primary_key=True)
    duration = sqla.Column(sqla.Integer)
    rating = sqla.Column(sqla.Float)
    
    genres = relationship(
        "GenreInDB",
        secondary=GenreInFilm,
    )
    def to_Film(self):
        return db.Film(self.title,self.duration,self.genres,self.rating)

class GenreInDB(Base):

    __tablename__ = 'genres'

    title = sqla.Column(sqla.String, primary_key=True)


class SqlAlchemyFilmStorage(db.FilmStorage):
    def __init__(self, backend):
        self.engine = create_engine(backend, echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind = self.engine)
    
    def _genre_to_class(self, session, genre):
        existing_genre = session.query(GenreInDB).filter(GenreInDB.title == genre).first()
        if not existing_genre:
            return GenreInDB(title = genre)
        return existing_genre

    def store(self, film):
        dict_film = film.to_dict()
        session = self.Session()
        genres_as_classes = [self._genre_to_class(session, title) for title in dict_film["genres"]]
        dict_film["genres"] = genres_as_classes
        film_in_db = FilmInDB(** dict_film)
        session.add(film_in_db)
        session.commit()

    def get_by_title(self, title):
        session = self.Session()
        result = session.query(FilmInDB).filter(FilmInDB.title == title).first()
        return result

    def get_all(self):
        session= self.Session()
        all_movies = session.query(FilmInDB).all()
        return [m.to_Film() for m in  all_movies]