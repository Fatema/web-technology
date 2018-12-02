from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/movies')
def get_movies():
    return jsonify([1,2,3])


if __name__ == '__main__':
    app.run()
