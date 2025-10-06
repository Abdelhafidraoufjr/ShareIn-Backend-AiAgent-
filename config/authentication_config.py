import os


class AuthConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    TOKEN_EXPIRATION_HOURS = int(os.getenv("TOKEN_EXPIRATION_HOURS"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    