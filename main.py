import json

import boto3
import requests
import configparser

from os import environ as env

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini")

    open_weather_api_key = env['OPENWEATHER_API_KEY']
    cities = config["Application"]['cities'].split(",")
    sqs_user = config["AWS-SQS"]

    client = boto3.client(
        'sqs',
        aws_access_key_id=env['SQS_ACCESS_KEY'],
        aws_secret_access_key=env['SQS_SECRET_KEY'],
        region_name=sqs_user['region'],
        endpoint_url=sqs_user['endpoint']
    )

    for city in cities:
        request = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_api_key}')
        content = request.json()
        response = {
            "lon": content['coord']['lon'],
            "lat": content['coord']['lat'],
            "main": content['weather'][0]['main'],
            "description": content['weather'][0]['description'],
            "feels_like": content['main']['feels_like'],
            "country": content['sys']['country'],
            "city": content['name'],
            "sunrise": content['sys']['sunrise'],
            "sunset": content['sys']['sunset']
        }
        client.send_message(
            QueueUrl=sqs_user['endpoint'],
            MessageBody=json.dumps(response)
        )
        print(
            f"Weather for country {content['sys']['country']} and "
            f"city {content['name']} has been successfully written to SQS")
