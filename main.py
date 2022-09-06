import configparser
import json
import uuid
from os import environ as env
from datetime import datetime

import boto3
import requests

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini")

    open_weather_api_key = env['OPENWEATHER_API_KEY']
    cities = config["Application"]['cities'].split(",")
    sqs_user = config["AWS-SQS"]

    queue_name = sqs_user['queue']

    sqs = boto3.resource(
        'sqs',
        region_name=sqs_user['region'],
        endpoint_url=sqs_user['endpoint'])
    client = sqs.get_queue_by_name(QueueName=queue_name)

    messages = []
    for city in cities:
        request = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_api_key}')
        content = request.json()
        response = {
            "Id": str(uuid.uuid4()),
            "MessageBody": json.dumps({
                "lon": content['coord']['lon'],
                "lat": content['coord']['lat'],
                "main": content['weather'][0]['main'],
                "description": content['weather'][0]['description'],
                "feels_like": content['main']['feels_like'],
                "country": content['sys']['country'],
                "date": datetime.fromtimestamp(content['dt']),
                "city": content['name'],
                "sunrise": content['sys']['sunrise'],
                "sunset": content['sys']['sunset']
            })
        }
        messages.append(response)
        print(
            f"Weather for country {content['sys']['country']} and "
            f"city {content['name']} has been successfully added to batch")

    client.send_messages(
        QueueUrl=sqs_user['endpoint'],
        Entries=messages
    )

    print(f'Batch has been successfully pushed to SQS queue {queue_name}')
