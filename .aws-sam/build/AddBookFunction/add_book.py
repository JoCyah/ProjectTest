import json
import boto3
import logging

# Initialize DynamoDB resource
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
        
        # Check if the body key exists in the event
        if 'body' not in event:
            raise KeyError('body')

        # Parse the request body
        body = json.loads(event['body'])
        if not isinstance(body, dict):
            raise ValueError("body is not a valid JSON object")

        book_id = body.get('book_id')
        title = body.get('title')
        author = body.get('author')
        cover_image = body.get('cover_image')

        # Check for required fields
        if not book_id or not title or not author or not cover_image:
            raise ValueError("Missing one or more required fields: 'book_id', 'title', 'author', 'cover_image'")

        # Insert the new book into the DynamoDB table
        table.put_item(
            Item={
                'book_id': book_id,
                'title': title,
                'author': author,
                'cover_image': cover_image
            }
        )

        # Return a success response
        return {
            'statusCode': 200,
            'body': json.dumps('Book added successfully!')
        }

    except KeyError as e:
        logger.error(f"Missing key in event: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps(f"Missing key: {str(e)}")
        }
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps(f"Invalid input: {str(e)}")
        }
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Internal server error: {str(e)}")
        }
