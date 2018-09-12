from flask import Flask
import flask

app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response


@app.route("/users", methods=['GET'])
def im_admin():
    return flask.jsonify(admin=True)


if __name__ == '__main__':
    app.run(port=8080)
