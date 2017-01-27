class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "changeitlater"
    SQLALCHEMY_DATABASE_URI = "postgres://user@ip/dbname"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "postgres://user@ip/dbname"
    TESTING = True

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "postgres://user@ip/dbname"
