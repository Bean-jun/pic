class Base(object):

    def __init__(self):
        self.DEBUG = False
        self.HOST = "http://192.168.1.100/"
        self.UPLOAD_FOLDER = "resource/uploads"
        self.FLASK_HOST = "0.0.0.0"
        self.FLASK_PORT = 8001


class Dev(Base):
    def __init__(self):
        super().__init__()
        self.DEBUG = True


class Product(Base):

    def __init__(self):
        super().__init__()
        self.DEBUG = False


ConfigMode = {
    "develop": Dev(),
    "product": Product(),
}
