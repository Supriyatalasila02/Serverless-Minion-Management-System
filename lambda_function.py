import json
import boto3

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    table = dynamodb.Table('Minion')

    if "MinionId" not in event:
        return {
            'statusCode': 400,
            'body': "MinionId is missing in the request body.",
            'headers': {
                'Content-Type': 'application/json',
            }
        }
    item = table.get_item(Key={'MinionId': event["MinionId"]}).get("Item", None)

    statusCode = 200

    if item is None:
        statusCode = 404
        body = f"Minion with id {event['MinionId']} not found"

    elif item["IsSummoned"] is True:
        body = f"Minion with id {event['MinionId']} is already summoned"

    else:
        item['IsSummoned'] = True
        table.put_item(Item=item)
        del item["IsSummoned"]
        body = item

    response = {
        'statusCode': statusCode,
        'body': body,
        'headers': {
            'Content-Type': 'application/json',
        }
    }

    return response
