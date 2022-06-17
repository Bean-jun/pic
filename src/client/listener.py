import os
import sys
import time

import click
import xerox

from tools import *

workspace = os.path.dirname(os.path.realpath(sys.argv[0]))
temp_file = os.path.join(workspace, "temp")


def gen_img_file_path():
    img_path = "img-%s.png" % datetime_add_time(
        format_datetime(format="%Y%m%d%H%M%S"),
        format_time())
    return os.path.join(temp_file, img_path)


@click.group
def cli():
    mkdir(temp_file)


@cli.command()
@click.option("--url", "-u", default="http://localhost/")
@click.option("--link", "-l", default="y", help="return http://xxxxx/xxx if link is y else ![](http://xxxxx/xxx)")
def once(url, link):
    """
    执行一次
    """
    print("开始执行....")
    status, msg = check_url(url)
    if not status:
        print(msg)
        return

    path = gen_img_file_path()
    img_path = saveImageGrab(path)
    if not img_path:
        print("剪贴板内容非图片")
        return

    status, filename_or_msg = check_file_allow(img_path)
    if not status:
        print(filename_or_msg)
        return

    data = read_file(img_path)
    filename = clean_filename(filename_or_msg)
    response = Request("POST", url, files={filename: data})
    response_txt = parse_response(response)

    if link == "y":
        xerox.copy(response_txt)
    else:
        xerox.copy("![%s](%s)" % (filename, response_txt))
    print("设置剪贴板成功")


@cli.command()
@click.option("--url", "-u", default="http://localhost/", help="upload server address")
@click.option("--link", "-l", default="y", help="return http://xxxxx/xxx if link is y else ![](http://xxxxx/xxx)")
@click.option("--sleep", "-s", default=2, help="program time sleep")
def more(url, link, sleep):
    """
    一直执行(推荐)
    """
    print("开始执行...")
    status, msg = check_url(url)
    if not status:
        print(msg)
        return

    while True:
        path = gen_img_file_path()
        img_path = saveImageGrab(path)
        if not img_path:
            # print("剪贴板内容非图片")
            time.sleep(sleep)
            continue

        status, filename_or_msg = check_file_allow(img_path)
        if not status:
            print(filename_or_msg)
            continue

        data = read_file(img_path)
        filename = clean_filename(filename_or_msg)
        response = Request("POST", url, files={filename: data})
        response_txt = parse_response(response)

        if link == "y":
            xerox.copy(response_txt)
        else:
            xerox.copy("![%s](%s)" % (filename, response_txt))
        print("设置剪贴板成功")

        time.sleep(sleep)


if __name__ == "__main__":
    cli()
