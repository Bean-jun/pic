import os

from flask import current_app, request
from flask.views import MethodView

from tools import *


class Resource(MethodView):

    def post(self, *args, **kwargs):
        try:
            for file in request.files:
                data = request.files.get(file)
                dst = os.path.join(current_app.config["UPLOAD_FOLDER"], file)
                data.save(dst)
            return trueReturn({"source": current_app.config["HOST"]+dst})
        except FileNotFoundError:
            mkdir(current_app.config["UPLOAD_FOLDER"])
            return falseReturn(message="please try again")
        except Exception as e:
            if current_app.config["DEBUG"] == True:
                print(e.args)
                msg = e.args
            else:
                msg = ""
            return falseReturn(msg)


def init_app(app):
    app.add_url_rule(rule="/", view_func=Resource.as_view("resource"))
