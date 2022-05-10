import csv
import os
from typing import List

from celery import Celery

from calculation import calculate_fare as calculation

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name='tasks.calculate_fare')
def calculate_fare() -> List:
    """
    Calculates the fares for the different rides
    """    
    return calculation()
