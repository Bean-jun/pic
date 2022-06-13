FROM    python:alpine
LABEL   email="1342104001@qq.com"
ENV     home /home
WORKDIR ${home}
COPY    src/server ${home}/server
COPY    requirements.txt ${home}
RUN     python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN     ["mkdir", "-p", "-m", "760", "resource/uploads"]
EXPOSE  8001
CMD     [ "python", "server/main.py"]