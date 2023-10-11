
import os
import datetime
basedir = os.path.abspath(os.path.dirname(__file__))

DB_NAME = "ticket_show.sqlite3"

class Config():
    DEBUG = True
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(SQLITE_DB_DIR, DB_NAME)
    
    SECRET_KEY = 'ds@324Dfg5d12wsa!2q@$5'
    JWT_SECRET_KEY = 'sd#@csdsmad2t223!$5'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1) 

    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"

    CELERY_BROKER_URL='redis://localhost:6379/1',
    CELERY_RESULT_BACKEND='redis://localhost:6379/2'

    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = 1000
    CACHE_KEY_PREFIX = 'task_api'
    CACHE_REDIS_URL = 'redis://localhost:6379/3'


