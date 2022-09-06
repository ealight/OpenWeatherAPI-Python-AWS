import configparser
import json
from decimal import Decimal

import boto3


def lambda_handler(event, context):
    config = configparser.ConfigParser()
    config.read("config.ini")

    db = boto3.resource('dynamodb')

    table_name = config['AWS-Dynamo']['table']

    table = db.Table(table_name)

    records = event['Records']

    with table.batch_writer() as batch:
        for record in records:
            message = json.loads(record['body'], parse_float=Decimal)
            message['id'] = record['messageId']
            batch.put_item(Item=message)

    return {
        'statusCode': 200,
        'itemCounts': len(records)
    }
