import os
import boto3
import json

sns = boto3.client('sns')
db = boto3.resource('dynamodb')
table_name = os.environ['DYNAMODB_TABLE']
sns_topic_arn = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):

    records = event['Records']
    table = db.Table(table_name)

    for record in records:

        dynamodb_data = record['dynamodb']
        event_name = record['eventName']

        if event_name == 'INSERT':
            new_item = dynamodb_data['NewImage']
            email = extract_value(new_item['email'])
            author = extract_value(new_item['author'])
            title = extract_value(new_item['title'])
            description = extract_value(new_item['description'])
            content = extract_value(new_item['content'])
            publish_time = extract_value(new_item['publishTime'])
            sentiment = extract_value(new_item['sentiment'])

            # delete_count = delete_data(table)
            # print(delete_data)
            

            message = f"Hi, this is a email notification for news\n " \
                f"The news information is:\n" \
                f"Author: {author}\n" \
                f"Title: {title}\n" \
                f"Description: {description}\n" \
                f"Content: {content}\n" \
                f"Published Time: {publish_time}\n" \
                f"The sentiment for the news is {sentiment}"

            print(message)
            try:
                
                response = sns.publish(TopicArn=sns_topic_arn, Message=message, Subject='News sentiment analysis')
                result = response['MessageId']
                statusCode = 200
                body = json.dumps({'Message': f'Message with {result} sent successfully'})
                

            except Exception as e:
                return {
                    'statusCode': 500,
                    'body': json.dumps({'Error': f"Message published failed with error {str(e)}"})
                }        

    return {
        'statusCode': statusCode,
        'body': body
    }


def extract_value(attribute):
    # key in the attribute dictionary
    data_type = list(attribute.keys())[0]

    # corresponding value in the attribute dictionary
    value = attribute[data_type]

    return value
