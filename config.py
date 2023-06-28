# from dotenv import load_dotenv
import os
# load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///my-database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


