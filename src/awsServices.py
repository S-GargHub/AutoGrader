import os
import boto3

# Create DynamoDB client
dynamodb = boto3.resource('dynamodb', 'us-west-2')

def check_exist_student_id(student_id):
    table = dynamodb.Table(os.environ.get('dynamo_table'))
    response = table.get_item(Key={'email': student_id})
    if 'Item' in response:
        return True
    return False

def update_score(student_id,grade):
    table = dynamodb.Table(os.environ.get('dynamo_table'))
    response = table.get_item(Key={'email': student_id})
    if 'Item' in response:
        best_score_str = response['Item']['best_score']
        best_score = float(best_score_str.strip('%'))
        if grade > best_score:
            table.put_item(
                    Item={
                        'email': student_id,
                        'best_score': str(grade)+'%'
                    }
                )

def add_score_dynamodb(student_id,best_score):
    table = dynamodb.Table(os.environ.get('dynamo_table'))
    table.put_item(
        Item={
            'email': student_id,
            'best_score': best_score,
        }
    )