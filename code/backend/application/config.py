# --------------------  Imports  --------------------

from application.globals import BACKEND_ROOT_PATH
import os

# --------------------  Code  --------------------


class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    db_path = os.path.join(
        BACKEND_ROOT_PATH, "databases", "supportTicketDB_Prod.sqlite3"
    )
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + db_path + "?charset=utf8"
    SECRET_KEY = "secretKey"
    DEBUG = False


class TestingConfig(Config):
    db_path = os.path.join(
        BACKEND_ROOT_PATH, "databases", "supportTicketDB_Test.sqlite3"
    )
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + db_path + "?charset=utf8"
    SECRET_KEY = "secretKey"
    DEBUG = True


class DevelopmentConfig(Config):
    db_path = os.path.join(
        BACKEND_ROOT_PATH, "databases", "supportTicketDB_Dev.sqlite3"
    )
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + db_path + "?charset=utf8"
    # SQLALCHEMY_ECHO = True # for sqlalchemy debug queries
    SECRET_KEY = "secretKey"
    DEBUG = True


# --------------------  END  --------------------