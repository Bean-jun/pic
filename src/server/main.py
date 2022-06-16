from flask import Flask


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    from view import init_app
    init_app(app)

    return app


app = create_app("config")

if __name__ == "__main__":
    # 开发时使用
    host = app.config["FLASK_HOST"]
    port = app.config["FLASK_PORT"]
    debug = True
    app.run(host, port, debug)
