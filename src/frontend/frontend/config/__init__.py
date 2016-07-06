import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../..', '.env')
load_dotenv(dotenv_path)

class Config(object):
    DEBUG = False
    TESTING = False
    MONGODB_URL = os.environ.get('MONGODB_URL', '127.0.0.1')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass
