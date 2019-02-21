import moviedb.db
from flask import Flask, request, render_template, redirect,url_for
from flask import jsonify
from wtforms import Form, BooleanField, SubmitField, StringField, PasswordField, validators, IntegerField, FloatField, TextAreaField
app = Flask(__name__)


class AddForm(Form):
    
    title = StringField('Title', [validators.required()])
    duration = IntegerField('Duration (min)') 
    rating = FloatField('rating')
    genres = TextAreaField('Genres(split by ; )')
    submit = SubmitField('Add film')

@app.route('/film/<wanted_film>')
def show_film(wanted_film):
    "loads json.database and returns a movie or all in json"
    print('looking for', wanted_film)  # for debug
    # populate a db
    empty_db = moviedb.db.MemoryFilmStorage()
    populated_db = moviedb.db.restore_database(empty_db, 'films.json')

    # define empty dict for result
    result = {}
    if wanted_film == '*':  # get all movies
        list_of_films = [film.to_dict() for film in populated_db]
        # save list_of_films to result with title as a key
        for film in list_of_films:
            result[film["title"]] = film
    else:  # return only wanted_film
        for film in populated_db:
            if film.title == wanted_film:
                result[wanted_film] = film.to_dict()
    # use flask.jsonify for return json
    return jsonify(**result)

@app.route('/add', methods=['GET', 'POST'])
def addFilm():
    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
        empty_db = moviedb.db.MemoryFilmStorage()
        populated_db = moviedb.db.restore_database(empty_db, 'films.json')
        film = moviedb.db.Film(form.title.data,form.duration.data,form.genres.data.split(";"),form.rating.data)
        populated_db.store(film)
        moviedb.db.save_database(populated_db,'films.json')
        return redirect(url_for('show_film', wanted_film = form.title.data))
    return render_template('add.html', form=form)
