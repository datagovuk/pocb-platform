import os
from dotenv import load_dotenv

#dotenv_path = os.path.join(os.path.dirname(__file__), '../../..', '.env')
#load_dotenv(dotenv_path)

class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass
