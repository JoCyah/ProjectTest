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
    Lambda function to list all books from the Books table in DynamoDB.

    Parameters:
    event (dict): The event dictionary.
    context (object): The context object containing runtime information.

    Returns:
    dict: The response dictionary with the status code and book summaries.
    """
    try:
        # Log the incoming event for debugging
        logger.info(f"Received event: {json.dumps(event)}")

        # Scan the DynamoDB table to retrieve all books
        response = table.scan()
        items = response.get('Items', [])

        # Extract relevant details (book_id, title, author) for each book
        book_summaries = [
            {
                'book_id': item['book_id'],
                'title': item['title'],
                'author': item['author']
            }
            for item in items
        ]

        # Return the book summaries in the response
        return {
            'statusCode': 200,
            'body': json.dumps(book_summaries)
        }

    except Exception as e:
        logger.error(f"Error processing event: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Internal server error: {str(e)}")
        }
