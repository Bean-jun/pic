# Markdown图床

<h2 style="text-align:center"><img src="./images/pic.png"></img></h2>

## 一、server

1. server配置

    修改`src/server/config.py`文件中`HOST`行，用于图床获取时的地址，你可以直接填写你的ip
## 二、client

1. client使用

    格式: client.py upload_server_address 文件地址

    例如：`./main http://192.168.1.100:8001/ xxx.png`

## 三、server启动

`docker-compose up -d --build`