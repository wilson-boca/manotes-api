from celery import Celery
from app import config

configuration = config.get_config()

celery = Celery('manotes_api', broker=configuration['REDIS_URL'])


def start_sending_email(email):
    start_sending_email(email)


@celery.task
def send_email(email):
    print(email)
