from main.celery_app import app as celery_app
from celery.utils.log import get_task_logger
from .utils import load_bike_info_to_dynamo, get_bike_info, camel_to_snake_as_dict
from .models import StateCenter

logger = get_task_logger(__name__)


@celery_app.task(bind=True)
def celery_load_bike_infos(self,  **kwargs):
    load_bike_info_to_dynamo()


@celery_app.task(bind=True)
def celery_load_bike_infos_to_rds(self,  **kwargs):
    bikes = get_bike_info()

    for bike in bikes:
        filtered = {k: v for k, v in
                    bike.items() if k in [
                        'stationId', 'rackTotCnt', 'parkingBikeTotCnt',
                        'stationLatitude', 'stationLongitude', 'stationName']}

        snaked_bike = camel_to_snake_as_dict(filtered)
        StateCenter.objects.create(**snaked_bike)
