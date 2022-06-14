from flask import Flask, current_app, request
from flask.views import MethodView
from config import ConfigMode

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(ConfigMode.get(config))

    from view import init_app
    init_app(app)

    return app


app = create_app("develop")

if __name__ == "__main__":
    host = app.config["FLASK_HOST"]
    port = app.config["FLASK_PORT"]
    debug = app.config["DEBUG"]
    app.run(host, port, debug)
