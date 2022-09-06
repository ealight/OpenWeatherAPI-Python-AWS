import configparser
from datetime import datetime
import json

import boto3


def lambda_handler(event, context):
    config = configparser.ConfigParser()
    config.read("config.ini")

    client = boto3.client('s3')

    bucket_name = config['AWS-S3']['bucket']

    records = event['Records']
    for record in records:
        data = record['dynamodb']
        unpacked_keys = unpack_dynamo_types(data['Keys'])

        country = unpacked_keys['country']
        record_id = unpacked_keys['id']

        if 'NewImage' in data:
            unpacked_body = unpack_dynamo_types(data['NewImage'])

            city = unpacked_body['city']
            date = datetime.fromisoformat(unpacked_body['date']).date()

            object_name = f"{country}-{city}-{date}-{record_id}.json"

            body = json.dumps(unpacked_body)
            client.put_object(Body=body, Bucket=bucket_name, Key=object_name)
            print(f'Successfully processed new weather for {country} - {city} with ID: {record_id}')
        else:
            print(f'Skipped processing deleted image for {country} with ID: {record_id}')

    return {
        'statusCode': 200,
        'itemsCounts': len(records)
    }


def unpack_dynamo_types(types):
    return {key: item
            for (key, value) in types.items()
            for (_, item) in value.items()}
