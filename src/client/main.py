import click
from tools import *


@click.command()
@click.option("--url", "-u", default="http://localhost/")
@click.argument("filelist", nargs=-1)
def cli(url, filelist):

    status, msg = check_url(url)
    if not status:
        print(msg)
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
