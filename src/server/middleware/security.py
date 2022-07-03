from flask import abort
from flask import request
from flask import current_app


def nginx_constraint_funs():
    """
    限制后端必须经过nginx转发
    """
    nginx_key = request.headers.get("X-PIC-NGINX", None)
    if nginx_key is None:
        abort(400)
    if nginx_key != current_app.config.get("NGINX_CONSTRAINT_KEY"):
        abort(400)


def pic_client_constraint_funs():
    """
    限制客户端
    """
    client_key = request.headers.get("X-PIC-CLIENT", None)
    if client_key is None:
        abort(400)
    if client_key != current_app.config.get("PIC_CLIENT_CONSTRAINT_KEY"):
        abort(400)

