import os

class config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret_key")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Diksha_Dristi.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False