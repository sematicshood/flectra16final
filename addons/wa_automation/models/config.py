import os


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    REDIS_URL = "redis://127.0.0.1:6379"