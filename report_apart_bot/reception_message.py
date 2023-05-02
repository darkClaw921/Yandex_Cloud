
import boto3
import os
import json


AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
queue_url = 'https://message-queue.api.cloud.yandex.net/b1gqkvs2rjugm2qkc9g5/dj600000000d1a2307bf/ddksta-queue1'

def send_message(message):


    # Create client
    client = boto3.client(
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        region_name='ru-central1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY 
    )

    # Create queue and get its url
    #queue_url = client.create_queue(QueueName='ddksta-queue').get('QueueUrl')
    #print('Created queue url is "{}"'.format(queue_url))

    # Send message to queue
    #mes = prepare(message)
    mes = message
    client.send_message(
        QueueUrl= queue_url,
        MessageBody=f'{mes}'
    )
    print('Successfully sent test message to queue ', mes)

    """
    # Receive sent message
    messages = client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        VisibilityTimeout=60,
        WaitTimeSeconds=20
    ).get('Messages')
    for msg in messages:
        print('Received message: "{}"'.format(msg.get('Body')))
    """
    # Delete processed messages
    """
    for msg in messages:
        client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=msg.get('ReceiptHandle')
        )
        print('Successfully deleted message by receipt handle "{}"'.format(msg.get('ReceiptHandle')))
    """

def handler(event, context):
    send_message(event)
    return {
        
        'statusCode': 200,
        'body': 'Передано в очередь',
    }
