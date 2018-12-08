import time

from flask import Flask, jsonify, render_template, request, redirect, url_for, json
from jinja2 import Environment

from service import Service

app = Flask(__name__, template_folder='templates')

# translations = get_gettext_translations()
# env = Environment(extensions=['jinja2.ext.i18n'])
# env.install_gettext_translations(translations)

service = Service()
logged_in = False
search_term = ""


# this is good enough just need to add random things for internationalization
# and call it a day with this one

@app.route('/', methods=['GET','POST'])
def main():
    global logged_in
    if request.method == 'GET':
        if logged_in:
            return redirect(url_for('get_movies'))
        else:
            return render_template("home.html")
    if request.method == 'POST':
        username = request.form.get('_username', "")
        password = request.form.get('_password', "")
        if service.login(username, password):
            logged_in = True
            return redirect(url_for('get_movies'))
        else:
            return render_template("home.html", login_fail=True)
    return render_template("home.html")


@app.route('/logout')
def logout():
    global logged_in
    logged_in = False
    return redirect(url_for('main'))


@app.route('/profile/', methods=['GET','POST'])
def update_user_profile():
    global logged_in
    rated_movies = get_json(service.get_rated_movies())
    if request.method == 'GET':
        genres = service.get_genres()
        user_static_data = service.get_user_static_data()
        return render_template("user-profile.html",
                               logged_in=logged_in,
                               genres=genres,
                               user=user_static_data,
                               ratings=rated_movies)
    elif request.method == 'POST':
        username = request.form.get('_username', "")
        password = request.form.get('_password', "")
        preferred_genres = request.form.getlist('_genres')
        if logged_in:
            service.update_preferred_genres(preferred_genres)
            service.update_user_data(username, password)
        else:
            service.create_profile(username, password, preferred_genres)
            logged_in = True
            return redirect(url_for('get_movies'))
        genres = service.get_genres()
        user_static_data = service.get_user_static_data()
        return render_template("user-profile.html",
                               logged_in=logged_in,
                               genres=genres,
                               user=user_static_data,
                               ratings=rated_movies,
                               success=True)


@app.route('/movie/<int:id>')
@app.route('/movie/<int:id>/<int:page>', methods=['GET','POST'])
def movie_page(id, page=1):
    if request.method == 'POST':
        rating = float(request.form.get('rating'))
        service.rate_movie(id, rating)
    elif request.method == 'GET':
        service.set_last_clicked_movie(id)
    reviews = get_json(service.get_movie_reviews(id, page))
    movie_data = get_json(service.get_movie(id))
    user_rating = service.get_movie_rating(id)
    if user_rating is None or user_rating.shape[0] == 0:
        rated = False
    else:
        user_rating = user_rating.iloc[0]['rating']
        rated = True
    print(rated)
    return render_template("movie.html",
                           reviews=reviews,
                           movie=movie_data,
                           user_rating=user_rating,
                           rated=rated,
                           page=page)


@app.route('/search/<int:page>')
@app.route('/search/')
def get_movies(page=1):
    global search_term
    term = request.args.get('term') or ""
    if term is "" and page > 1:
        term = search_term
    else:
        search_term = term
    _, recommended_movies = service.get_recommendations()
    recommended_movies = get_json(recommended_movies)
    extra_recommened_movies = get_json(service.get_extra_recommendations())
    if len(extra_recommened_movies) == 0:
        last_clicked_movie = ""
    else:
        last_clicked_movie = service.get_movie().iloc[0]['title']
    all_movies = get_json(service.search_movies(term, page=page))
    return render_template("movies.html",
                           recommended_movies=recommended_movies,
                           extra_recommened_movies=extra_recommened_movies,
                           movie_name=last_clicked_movie,
                           all_movies=all_movies,
                           page=page,
                           term=search_term)


def get_json(dataframe):
    return json.loads(dataframe.to_json(orient='records'))


@app.template_filter('ctime')
def timectime(s):
    return time.ctime(s)

if __name__ == '__main__':
    app.run()
