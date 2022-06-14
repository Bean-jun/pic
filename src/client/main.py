import os
import sys
import requests


# 文件白名单
FILE_EXT_LIST = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif"
}


def Request(method, url, data=None, json=None, **kwargs):
    response = requests.request(method=method,
                                url=url,
                                data=data,
                                json=json,
                                **kwargs)
    return response


def main():
    args = sys.argv

    if len(args) < 1:
        print("please set upload file")
        return

    if not args[1].startswith("http"):
        print("please set upload address")
        return

    URL = args[1]

    for file in args[2:]:
        filename, ext = os.path.splitext(file)
        if ext.lower() not in FILE_EXT_LIST:
            print("current not allow")
            return

        with open(file, "rb") as f:
            data = f.read()
        filename = "%s%s" % (filename.rsplit("/", 1)[-1], ext)
        response = Request("POST", URL, files={filename: data})
        if response.status_code == 200:
            data = response.json()
            print((data.get("data") or {}).get("source"))
            return (data.get("data") or {}).get("source")
        else:
            print("")
            return ""


if __name__ == "__main__":
    main()
