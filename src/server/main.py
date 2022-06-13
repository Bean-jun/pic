import os
from flask import Flask, current_app, request
from flask.views import MethodView

from tools import *

Server_Address_Host = "http://192.168.1.100/"

app = Flask(__name__)
UPLOAD_FOLDER = 'resource/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Resource(MethodView):

    def post(self, *args, **kwargs):
        try:
            for file in request.files:
                data = request.files.get(file)
                dst = os.path.join(UPLOAD_FOLDER, file)
                data.save(dst)
            return trueReturn({"source": Server_Address_Host+dst})
        except Exception as e:
            if current_app.config["DEBUG"] == True:
                print(e.args)
                msg = e.args
            else:
                msg = ""
            return falseReturn(msg)


app.add_url_rule(rule="/", view_func=Resource.as_view("resource"))

if __name__ == "__main__":
    app.run("0.0.0.0", 8001, True)
