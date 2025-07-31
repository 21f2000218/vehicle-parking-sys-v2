from celery import Celery

from app.config import Config

config = Config()

def make_celery(app=__name__):

    backend = config.CELERY_RESULT_BACKEND
    broker = config.CELERY_BROKER_URL
    beat = config.CELERY_BEAT_SCHEDULE
    return Celery(app, backend=backend, broker=broker, beat=beat)


celery = make_celery()