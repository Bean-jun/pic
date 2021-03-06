FROM    python:alpine
LABEL   email="1342104001@qq.com"
ENV     TZ Asia/Shanghai
ENV     home /home
WORKDIR ${home}
COPY    src/server ${home}/server
COPY    requirements_server.txt ${home}
RUN     python -m pip install -r requirements_server.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE  8001
WORKDIR ${home}/server
CMD     [ "gunicorn", "--config=gunicorn_conf.py", "main:app"]