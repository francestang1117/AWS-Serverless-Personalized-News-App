import json
import os
import uuid
import boto3
import requests


comprehend_client = boto3.client('comprehend')

db_client = boto3.resource('dynamodb')

table_name = os.environ['DYNAMODB_TABLE']
# Get the table
table = db_client.Table(table_name)
sns = boto3.client('sns')
sns_topic_arn = os.environ['SNS_TOPIC_ARN']

headers = {
    "Content-Type": "application/json",
     "Access-Control-Allow-Origin": "*", 
     "Access-Control-Allow-Credentials": "true"
}

def lambda_handler(event, context):

    if 'body' in event:
        info = json.loads(event['body'])
    else:
        return {
            'headers': headers,
            'statusCode': 500,
            'body': json.dumps({'Error': 'no input parameters to get news'})
        } 

    if 'email' in info:
        email = info['email']
        is_subscribed = False
        
        response = sns.list_subscriptions_by_topic(TopicArn=sns_topic_arn)
        print("sub list is ", response)
        for subscription in response['Subscriptions']:
            if subscription['Protocol'] == 'email' and subscription['Endpoint'] == email:
                if subscription['SubscriptionArn'] != "PendingConfirmation":
                    is_subscribed = True
                    break
                else:
                   return {
                       'headers': headers,
                        'statusCode': 400,
                        'body': json.dumps({'Error': 'Please the subscribe email'})
                   }

        if not is_subscribed:

        # If the loop completes without finding a subscription, it means the email is not subscribed
            sns.subscribe(TopicArn=sns_topic_arn, Protocol='email', Endpoint=email)
            
        remove_previous_subsribers(email)

    else:
        return {
            'headers': headers,
            'statusCode': 500,
            'body': json.dumps({'Error': 'no user email'})
        }       

    # Get the endpoint
    if 'endpoint' in info:
        endpoint = info['endpoint']
    else:
        return {
            'headers': headers,
            'statusCode': 500,
            'body': json.dumps({'Error': 'no endpoint to get news'})
        } 

    # Get parameters
    if 'parameters' in info:
        parameters = info.get('parameters', {})

    else:
        parameters = {'apiKey': 'c532d3f8b384465c8d4b66feba3a5c5d'}

    # Add required parameter apiKey
    parameters['apiKey'] = 'c532d3f8b384465c8d4b66feba3a5c5d'

    
    response = requests.get(f'https://newsapi.org/v2/{endpoint}', params=parameters)

    if response.json().get('status') != 'ok':
        error = response.json().get('message')
        return {
            'headers': headers,
            'statusCode': response.status_code,
            'body': json.dumps({'Error': f'Have other errors: {error}'})
        }

    # Delete the first 10 older items
    # delete_data()

    articles_with_sentiments = []

    # get the first 20 articles
    for article in response.json()['articles'][:10]:
        author = article['author']
        title = article['title']
        description = article['description']
        content = article['content']
        publish_time = article['publishedAt']

        if content is None:
            sentiment = get_sentiment(title)
        else:
            sentiment = get_sentiment(content)

        if sentiment['statusCode'] == 200:
            sentiment_data = sentiment['body']

            res = insertDataToDyamodb(email, author, title, description, content, publish_time, sentiment_data['sentiment']['Sentiment'])
            if res['statusCode'] == 200:
                print('Successfully insert data into table')

                articles_with_sentiments.append({
                    'sentiment': sentiment_data['sentiment']['Sentiment'],
                    'news': {
                        'author': author,
                        'title': title,
                        'description': description,
                        'content': content,
                        'publish_time': publish_time
                    }
                })
            else:
                
                error = res['body'].get('Error')
                return {
                    'headers': headers,
                    'statusCode': 500,
                    'body': json.dumps({'Error': f'Store data failed with error {str(error)}'})
            }
        else:
            error_res = json.loads(res['body'])
            error = error_res.get('Error')
            return {
                'headers': headers,
                'statusCode': 500,
                'body': json.dumps({'Error': f'Get sentiment failed with error {str(error)}'})
            }

    print('Successfully return all the data')

    return {
        'headers': headers,
        'statusCode': 200,
        'body': json.dumps({'articles_with_sentiments': articles_with_sentiments})
    }   
    


def insertDataToDyamodb(email, author, title, description, content, publish_time, sentiment):
    # insert data into table
    data = {
        'id': str(uuid.uuid4()),
        'email': email,
        'author': author,
        'title': title,
        'description': description,
        'content': content,
        'publishTime': publish_time,
        'sentiment': sentiment
    }

    try:
        body = table.put_item(Item = data)
        statusCode = 200

    except Exception as e:
        statusCode = 400
        body = {'Error': str(e)}
    
    return {
        'statusCode': statusCode,
        'body': body
    }

def detect_language(news_content):
    response = comprehend_client.detect_dominant_language(Text=news_content)
    highest_score = 0
    dominant_language = ""
    for language in response['Languages']:
        if language['Score'] > highest_score:
            highest_score = language['Score']
            dominant_language = language['LanguageCode']
    return dominant_language

# process the news using comprehend
def get_sentiment(news_content):

    language = detect_language(news_content)

    parameters = {
        "TextList": [news_content],
        "LanguageCode": language
    }

    try:

        entities = comprehend_client.batch_detect_entities(**parameters)
        entity = entities['ResultList'][0]

        sentiments = comprehend_client.batch_detect_sentiment(**parameters)
        sentiment = sentiments['ResultList'][0]

        statusCode = 200
        body = {
            'entity': entity,
            'sentiment': sentiment
        }

    except Exception as e:
        statusCode = 400
        body = {'Error': str(e)}

        return {
            'statusCode': statusCode,
            'body': body
        }

    return {
        'statusCode': statusCode,
        'body': body
    }

def remove_previous_subsribers(current_user_email):

    response = sns.list_subscriptions_by_topic(TopicArn=sns_topic_arn)
    
    # List to store emails of subscribers who need to be removed
    emails_to_remove = []

    # Get emails of all current subscribers
    current_subscribers = set([subscription['Endpoint'] for subscription in response['Subscriptions']])
    print("subscribers are ", ' '.join(map(str, current_subscribers)))
    
    for subscriber_email in current_subscribers:
        print("the current user is ", current_user_email)
        if subscriber_email != current_user_email:
            emails_to_remove.append(subscriber_email)

    # Remove the previous subscribers who are not the current user
    for email_to_remove in emails_to_remove:
        # Get the SubscriptionArn for a given email
        
        subscription_arn = get_subscription_arn(sns_topic_arn, email_to_remove)
        print("the arn is ", subscription_arn)
        if subscription_arn and subscription_arn != "PendingConfirmation":
            print("the unsubscribe arn should be ", subscription_arn)
            sns.unsubscribe(SubscriptionArn=subscription_arn)

def get_subscription_arn(sns_topic_arn, email):
    # Get the SubscriptionArn for a given email
    response = sns.list_subscriptions_by_topic(TopicArn=sns_topic_arn)
    print(json.dumps(response))
    for subscription in response['Subscriptions']:
        if subscription['Protocol'] == 'email' and subscription['Endpoint'] == email:
            print("sub arn is ", subscription['SubscriptionArn'])
            return subscription['SubscriptionArn']
    return None

    














   

    