import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = True
    TESTING = False


class DevelopmentConfig(Config):
    SECRET = os.getenv("SECRET_KEY")
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY")


config = {
    "development": DevelopmentConfig,
    "testing": DevelopmentConfig,
    "production": DevelopmentConfig,
}
