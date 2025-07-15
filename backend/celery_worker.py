from celery import Celery
from config import Config

def create_celery_app():
    celery = Celery(
        'quiz_master',
        broker=Config.CELERY_BROKER_URL,
        backend=Config.CELERY_RESULT_BACKEND
    )
    celery.conf.timezone = 'Asia/Kolkata'
    return celery

celery = create_celery_app()
