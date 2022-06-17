import os

import click
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


def clean_filename(path):
    return path.rsplit("/", 1)[-1]


def parse_response(response):
    if response.status_code == 200:
        data = response.json()
        return (data.get("data") or {}).get("source")
    else:
        return ""


@click.command()
@click.option("--url", "-u", default="http://localhost/")
@click.argument("filelist", nargs=-1)
def cli(url, filelist):

    if not url.startswith("http"):
        print("please set upload address")
        return

    for file in filelist:
        status, filename_or_msg = check_file_allow(file)
        if not status:
            print(filename_or_msg)
            return

        data = read_file(file)
        filename = clean_filename(filename_or_msg)
        response = Request("POST", url, files={filename: data})
        response_txt = parse_response(response)
        print(response_txt)


if __name__ == "__main__":
    cli()
