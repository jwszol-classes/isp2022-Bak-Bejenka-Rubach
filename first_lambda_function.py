import json
from opensky_api import OpenSkyApi
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Flights')

def lambda_handler(event, context):
    i = 0

    api = OpenSkyApi()

    states = api.get_states(bbox=(49.00, 54.50, 14.07, 24.09))

    for s in states.states:
        table.put_item(
            Item={
                'numer': str(i),
                'latitude': str(s.latitude),
                'longitude': str(s.longitude)
            }    
        )
        i = i + 1

    response = {
        'message':  'Item added'
    }

    return {
        'statusCode': 200,
        'body': response
    }