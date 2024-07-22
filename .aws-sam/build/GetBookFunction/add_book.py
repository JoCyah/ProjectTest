import json
import boto3
import logging
import uuid

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Books')

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function to add a book to the Books table in DynamoDB.

    Parameters:
    event (dict): The event dictionary containing the book details in the body.
    context (object): The context object containing runtime information.

    Returns:
    dict: The response dictionary with the status code and message.
    """
    try:
        # Log the incoming event for debugging
        logger.info(f"Received event: {json.dumps(event)}")

        # Parse the body from the event
        body = json.loads(event['body'])

        # Generate a unique book_id if not provided
        book_id = body.get('book_id', str(uuid.uuid4()))

        # Prepare the item to be put into DynamoDB
        item = {
            'book_id': book_id,
            'title': body['title'],
            'author': body['author'],
            'cover_image': body.get('cover_image', '')
        }

        # Put the item into the DynamoDB table
        table.put_item(Item=item)

        # Return a success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps('Book added successfully!')
        }

    except KeyError as e:
        logger.error(f"Missing key in event: {e}")
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(f"Missing key: {str(e)}")
        }
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(f"Internal server error: {str(e)}")
        }
