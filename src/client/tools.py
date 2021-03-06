import datetime
import os
import sys
import time

import requests
from PIL import ImageGrab

# 后端支持的请求头设置
X_PIC_CLIENT = "2d7d584ee8af25622c4b0ae3afa850acdf9e3d03"
# 文件白名单
FILE_EXT_LIST = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif"
}


def _Request(method, url, data=None, json=None, **kwargs):
    response = requests.request(method=method,
                                url=url,
                                data=data,
                                json=json,
                                **kwargs)
    return response

def Request(method, url, data=None, json=None, **kwargs):
    headers = {"X-PIC-CLIENT": X_PIC_CLIENT}
    if hasattr(kwargs, "headers") and isinstance(getattr(kwargs, "headers"), dict):
        kwargs.get("headers").update(headers)
    else:
        kwargs.update({"headers": headers})
    return _Request(method, url, data=None, json=None, **kwargs)


def Ping(method, url, **kwargs):
    response = Request(method, url, **kwargs)
    if response.status_code == 200:
        return True
    return False


def read_file(path, mode="rb"):
    with open(path, mode) as f:
        return f.read()


def check_file(path):
    return os.path.isfile(path)


def check_file_allow(path):
    if not check_file(path):
        return False, "非文件类型"
    filename, ext = os.path.splitext(path)
    if ext.lower() not in FILE_EXT_LIST:
        return False, "非图片类型"
    return True, "%s%s" % (filename, ext)


def check_url(url):
    if not url.startswith("http"):
        return False, "please set upload address"
    return True, ""


def clean_filename(path):
    if sys.platform == "win32":
        return path.rsplit("\\", 1)[-1]
    return path.rsplit("/", 1)[-1]


def parse_response(response):
    if response.status_code == 200:
        data = response.json()
        return (data.get("data") or {}).get("source")
    else:
        return ""


def format_datetime(time=datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S"):
    return time.strftime(format)


def format_time(time=time.time()):
    return str(int(time))


def datetime_add_time(datetime_str, time_str):
    return "%s%s" % (datetime_str, time_str)


def mkdir(dir):
    try:
        os.makedirs(dir)
    except Exception as e:
        pass


def saveImageGrab(path):
    img = ImageGrab.grabclipboard()
    if img is None:
        return
    img.save(path, "PNG")
    return path
