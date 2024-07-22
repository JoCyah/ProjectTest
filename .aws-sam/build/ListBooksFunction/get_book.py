import json
import boto3
import logging

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Books')

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function to retrieve a book from the Books table in DynamoDB.

    Parameters:
    event (dict): The event dictionary containing the book ID in the path parameters.
    context (object): The context object containing runtime information.

    Returns:
    dict: The response dictionary with the status code and book details.
    """
    try:
        # Log the incoming event for debugging
        logger.info(f"Received event: {json.dumps(event)}")

        # Get the book ID from the path parameters
        book_id = event['pathParameters']['book_id']

        # Retrieve the book from the DynamoDB table
        response = table.get_item(
            Key={
                'book_id': book_id
            }
        )

        # Check if the book was found
        if 'Item' in response:
            # Return the book details in the response
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
            }
        else:
            # Return a not found response if the book does not exist
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Book not found'})
            }

    except KeyError as e:
        logger.error(f"Missing key in event: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps(f"Missing key: {str(e)}")
        }
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Internal server error: {str(e)}")
        }
