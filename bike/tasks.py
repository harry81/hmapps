from main.celery_app import app as celery_app
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from celery.utils.log import get_task_logger
from .utils import get_bike_info, camel_to_snake_as_dict
from .models import StateCenter

logger = get_task_logger(__name__)


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


@celery_app.task(bind=True)
def celery_bike_report(self,  **kwargs):

    subject = '%s - Daily bike report' % datetime.now().strftime('%Y-%m-%d')
    from_email, to = 'chharry@gmail.com', 'chharry@gmail.com'
    text_content = ''
    html_content = 'number of statecenter %d' % StateCenter.objects.count()

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
