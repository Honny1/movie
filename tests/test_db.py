import moviedb.db
import moviedb.sqla
import os

def test_film():
    film = moviedb.db.Film("Fantomas", 120, ["action"])
    assert film.title == "Fantomas"


def test_memory_db():
    db = moviedb.db.MemoryFilmStorage()
    any_db_basic_test(db)


def test_sqlite_db():
    db = moviedb.db.SqliteFilmStorage()
    any_db_basic_test(db)
    db.close()


def test_sqlAlchemy_db():
    filename="sqla.db"
    os.remove(filename)
    backend=f"sqlite:///{filename}"
    db = moviedb.sqla.SqlAlchemyFilmStorage(backend)
    any_db_basic_test(db)
    
def any_db_basic_test(db):
    store_fantomas_to_db(db)
    store_fantomas2_to_db(db)
    assert fantomas_in_db(db)
    assert db.get_by_title("Franta") is None


def store_fantomas_to_db(db):
    film = moviedb.db.Film("Fantomas", 120, ["action"])
    db.store(film)

def store_fantomas2_to_db(db):
    film = moviedb.db.Film("Fantomas2", 120, ["action"])
    db.store(film)


def fantomas_in_db(db):
    film = db.get_by_title("Fantomas")
    return film.title == "Fantomas"


def test_film_comparison():
    film1 = moviedb.db.Film("Fantomas", 120, ["action"])
    film2 = moviedb.db.Film("Fantomas", 120, ["action"])
    assert film1 == film2
    assert film1.__eq__(film2)

def test_different_film_comparison():
    film1 = moviedb.db.Film("Fantomas2", 123, ["sci-fi"])
    film2 = moviedb.db.Film("Fantomas", 123, ["sci-fi"])
    film3 = moviedb.db.Film("Fantomas2", 120, ["sci-fi"])
    film4 = moviedb.db.Film("Fantomas2", 123, ["action"])
    film5 = moviedb.db.Film("Fantomas2", 123, ["sci-fi"],5)
    assert film1 != film2
    assert False == film1.__eq__(film2)
    assert False == film1.__eq__(film3)
    assert False == film1.__eq__(film4)
    assert False == film1.__eq__(film5)


def test_film_save_and_restore_as_dict():
    film = moviedb.db.Film("Fantomas", 120, ["action","comedy"])
    film_as_dict = film.to_dict()
    film_from_dict = moviedb.db.Film.from_dict(film_as_dict)
    assert film == film_from_dict


def test_memory_save_and_restore():
    db1 = moviedb.db.MemoryFilmStorage()
    db2 = moviedb.db.MemoryFilmStorage()
    any_save_and_restore(db1, db2)

def test_sql_save_and_restore():
    db1 = moviedb.db.SqliteFilmStorage()
    db2 = moviedb.db.SqliteFilmStorage()
    any_save_and_restore(db1, db2)


def any_save_and_restore(save_db, restore_db):
    assert save_db is not restore_db

    store_fantomas_to_db(save_db)

    film = moviedb.db.Film("Fantomas 2", 120, ["action","comedy"])
    save_db.store(film)

    moviedb.db.save_database(save_db, "dbfile")

    moviedb.db.restore_database(restore_db, "dbfile")

    assert fantomas_in_db(restore_db)

    film = restore_db.get_by_title("Fantomas 2")
    assert film.title == "Fantomas 2"
    assert film.genres == set(["action","comedy"])