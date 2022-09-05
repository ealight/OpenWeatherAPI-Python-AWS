import configparser
import json
from collections import ChainMap
from decimal import Decimal

import boto3


def lambda_handler(event, context):
    config = configparser.ConfigParser()
    config.read("config.ini")

    db = boto3.resource('dynamodb')

    table_name = config['AWS-Dynamo']['table']

    table = db.Table(table_name)

    records = event['Records']

    for record in records:
        body = json.loads(record['body'], parse_float=Decimal)
        table.put_item(
            Item=dict(ChainMap({'id': record['messageId']}, body))
        )

    return {
        'statusCode': 200,
        'itemCounts': len(records)
    }
