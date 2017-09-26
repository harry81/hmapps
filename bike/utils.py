import re
import requests
from datetime import datetime


url_bike = 'https://www.bikeseoul.com/app/station/getStationRealtimeStatus.do'


def camel_to_snake(name):
    """ Convert text in camel string to in snake
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def camel_to_snake_as_dict(obj):
    rlt = {}
    for key in obj:
        rlt[camel_to_snake(key)] = obj.get(key)

    return rlt


def put_item(table, item):
    filtered = {k: v for k, v in
                item.items() if k in [
                    'when',
                    'stationId', 'rackTotCnt', 'parkingBikeTotCnt',
                    'stationLatitude', 'stationLongitude', 'stationName']}
    table.put_item(Item=filtered)


def get_bike_info():
    res = requests.get(url_bike)
    rlt = []

    for ele in res.json()['realtimeList']:
        ele['when'] = datetime.strftime(datetime.now(), "%y%m%d:%H%M")
        ele.pop('stationImgFileName')
        rlt.append(ele)

    return rlt
