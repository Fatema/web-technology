from flask import Flask, jsonify, render_template

from API.model import RecommendationSystem

app = Flask(__name__)

m_rec = RecommendationSystem()

@app.route('/')
def main():
    return render_template('templates/index.html', movies=m_rec.movies)


@app.route('/movies')
def get_movies():
    return jsonify([1,2,3])


if __name__ == '__main__':
    app.run()
