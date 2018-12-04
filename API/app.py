from flask import Flask, jsonify, render_template, request
from jinja2 import Environment

from API.recommendation_engine import RecommendationEngine

app = Flask(__name__)

# translations = get_gettext_translations()
# env = Environment(extensions=['jinja2.ext.i18n'])
# env.install_gettext_translations(translations)

logged_in = False

@app.route('/')
def main():
    return render_template("home.html", login_fail=False)


@app.route('/login')
def validate_user():
    username = request.args.get('file')
    return None


@app.route('/profile/<int:userId>')
def get_user_profile(userId):
    print(request.method)
    if request.method == 'POST':
        if request.form.get('Encrypt') == 'Encrypt':
            # pass
            print("Encrypted")
        elif request.form.get('Decrypt') == 'Decrypt':
            # pass # do something else
            print("Decrypted")
        else:
            # pass # unknown
            return render_template("index.html")
    elif request.method == 'GET':
        # return render_template("index.html")
        print("No Post Back Call")
    return None


@app.route('/profile/new')
def create_user_profile():
    return jsonify([1,2,3])


@app.route('/search/<term>')
def get_movies(term):
    return None


if __name__ == '__main__':
    app.run()
