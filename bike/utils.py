import boto3
import requests
from datetime import datetime
from django.conf import settings


dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.REGION_NAME)

url_bike = 'https://www.bikeseoul.com/app/station/getStationRealtimeStatus.do'


def create_table(table):
    table = dynamodb.create_table(
        TableName=table,
        KeySchema=[
            {
                'AttributeName': 'stationId',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'when',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'when',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'stationId',
                'AttributeType': 'S'
            },

            ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=table)

    return table


def put_item(table, item):
    filtered = {k: v for k, v in
                item.items() if k in [
                    'when',
                    'stationId', 'rackTotCnt', 'parkingBikeTotCnt',
                    'stationLatitude', 'stationLongitude', 'stationName']}
    table.put_item(Item=filtered)


def get_bike_info(table):
    res = requests.get(url_bike)
    rlt = []

    for ele in res.json()['realtimeList']:
        ele['when'] = datetime.strftime(datetime.now(), "%y%m%d:%H%M")
        ele.pop('stationImgFileName')
        rlt.append(ele)

    return rlt


def load_bike_info_to_dynamo():
    table_name = 'db_bikes'
    bike_table = dynamodb.Table(table_name)

    try:
        bike_table.table_status

    except:
        bike_table = create_table(table_name)

    bikes = get_bike_info(bike_table)
    for ele in bikes:
        put_item(bike_table, ele)
