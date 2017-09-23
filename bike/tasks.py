from main.celery_app import app as celery_app
from celery.utils.log import get_task_logger
from .utils import load_bike_info_to_dynamo

logger = get_task_logger(__name__)


@celery_app.task(bind=True)
def celery_load_bike_infos(self,  **kwargs):
    load_bike_info_to_dynamo()
