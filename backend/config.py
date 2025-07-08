import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour how does this tie with expire delta in login route??
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz_master.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
