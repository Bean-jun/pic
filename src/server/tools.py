import os
from flask import jsonify


def trueReturn(data="", code=200, message="success"):
    return jsonify({
        "data": data,
        "code": code,
        "message": message
    })


def falseReturn(data="", code=400, message="faile"):
    return jsonify({
        "data": data,
        "code": code,
        "message": message
    })


def mkdir(dir):
    try:
        os.makedirs(dir)
    except Exception as e:
        pass


def clean_path(path):
    if "\\" in path:
        return path.replace("\\", "/")
    return path
