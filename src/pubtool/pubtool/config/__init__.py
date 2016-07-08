import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../..', '.env')
load_dotenv(dotenv_path)

class Config(object):
    DEBUG = False
    TESTING = False
    ELASTIC_HOSTS = os.environ.get('ELASTIC_HOSTS', '["127.0.0.1"]')
    MONGO_HOST = os.environ.get('MONGODB_URL', '127.0.0.1')

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass
