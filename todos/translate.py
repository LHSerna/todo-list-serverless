import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')
translate = boto3.client('translate')


def newlanguage(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    #Comprehend auto mode
    source_language = "auto"
    #Translate
    target_language = event['pathParameters']['language']

    # fetch todo from the database
    response = table.get_item(
        Key={
           'id': event['pathParameters']['id']
        }
    )
    
    result = {
        'NewText': translate.translate_text(Text=response['Item']['text'],
        SourceLanguageCode=source_language, 
        TargetLanguageCode=target_language)
    }

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['NewText'])
    }

    return response
