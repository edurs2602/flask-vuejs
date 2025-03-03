import os


class BaseConfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    DEBUG = os.getenv("DEBUG", "True") == "True"

    MONGODB_DB = os.getenv("DB_NAME", "admin")
    MONGODB_HOST = os.getenv("DB_HOST", "mongo")
    MONGODB_PORT = int(os.getenv("DB_PORT", 27017))
    MONGODB_USERNAME = os.getenv("DB_USER", "root")
    MONGODB_PASSWORD = os.getenv("DB_PASS", "root")

    MONGO_URI = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB}?authSource=admin"
