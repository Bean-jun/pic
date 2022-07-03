from flask import Flask


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # 中间件
    from middleware import security, error
    app.before_request(security.nginx_constraint_funs)
    app.before_request(security.pic_client_constraint_funs)
    app.register_error_handler(400, error.error_400)
    app.register_error_handler(500, error.error_500)

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
