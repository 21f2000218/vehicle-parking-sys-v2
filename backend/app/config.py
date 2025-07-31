from flask import Flask
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    print(os.environ.get("FLASK_RUN_HOST"))
    print(os.environ.get("SQLALCHEMY_DATABASE_URI"))
    FLASK_RUN_HOST = os.environ.get("FLASK_RUN_HOST")
    FLASK_RUN_PORT = os.environ.get("FLASK_RUN_PORT")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", False)
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    # TASKS_ALWAYS_EAGER = True
    CELERY_BEAT_SCHEDULE = {
        'send-daily-reminders': {
            'task': 'utils.celery_task.daily_reminder.daily_reminders',
            'schedule': 60.0,
        },
        'send-monthly-reports': {
            'task': 'utils.celery_task.monthly_report.monthly_reports',
            'schedule': 60.0,
        },
    }
    CACHE_TYPE = 'redis'
    SESSION_TYPE = 'filesystem'
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL', 'redis://localhost:6379/1')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_IDENTITY_CLAIM = "user_id"  # default == sub
    JWT_ACC_TOKEN_EXPIRES = timedelta(minutes=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=2)
    # CORS_SUPPORTS_CREDENTIALS = True