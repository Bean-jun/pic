# server
DEBUG = False
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 8001

# python3 -c "import secrets, random;print(secrets.token_hex(random.randint(16, 20)))"
# nginx 约束key, 这里需要和nginx配置请求头设置一致
NGINX_CONSTRAINT_KEY = "c2dae3cd58c70db6d438bdcf6b16d0bb67199374"
# pic 约束key, 这里需要客户端和服务端设置一致
PIC_CLIENT_CONSTRAINT_KEY = "2d7d584ee8af25622c4b0ae3afa850acdf9e3d03"

# 服务器配置
HOST = "http://192.168.1.100/"
UPLOAD_FOLDER = "resource/uploads"
