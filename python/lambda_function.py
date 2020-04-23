import json
import image_processing

def lambda_handler(event, context):
    original_image = event['body']

    result_image = image_processing.launch_image_processing(original_image)
    
    # TODO implement
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(result_image)
    }
