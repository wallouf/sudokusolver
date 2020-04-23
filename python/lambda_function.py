import json

def lambda_handler(event, context):
    original_image = event['body']
    
    # TODO implement
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(original_image)
    }
