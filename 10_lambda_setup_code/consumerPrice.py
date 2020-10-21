import json
import boto3
import botocore
import pandas as pd
import boto3
from io import StringIO
import io

#S3 BUCKET
REGION = "us-east-2"

### SQS Utils###
def sqs_queue_resource(queue_name):
    """Returns an SQS queue resource connection

    Usage example:
    In [2]: queue = sqs_queue_resource("dev-job-24910")
    In [4]: queue.attributes
    Out[4]:
    {'ApproximateNumberOfMessages': '0',
     'ApproximateNumberOfMessagesDelayed': '0',
     'ApproximateNumberOfMessagesNotVisible': '0',
     'CreatedTimestamp': '1476240132',
     'DelaySeconds': '0',
     'LastModifiedTimestamp': '1476240132',
     'MaximumMessageSize': '262144',
     'MessageRetentionPeriod': '345600',
     'QueueArn': 'arn:aws:sqs:us-west-2:414930948375:dev-job-24910',
     'ReceiveMessageWaitTimeSeconds': '0',
     'VisibilityTimeout': '120'}

    """

    sqs_resource = boto3.resource('sqs', region_name=REGION)
    log_sqs_resource_msg = "Creating SQS resource conn with qname: [%s] in region: [%s]" %\
     (queue_name, REGION)
    queue = sqs_resource.get_queue_by_name(QueueName=queue_name)
    return queue

def sqs_connection():
    """Creates an SQS Connection which defaults to global var REGION"""

    sqs_client = boto3.client("sqs", region_name=REGION)
    log_sqs_client_msg = "Creating SQS connection in Region: [%s]" % REGION
    return sqs_client

def sqs_approximate_count(queue_name):
    """Return an approximate count of messages left in queue"""

    queue = sqs_queue_resource(queue_name)
    attr = queue.attributes
    num_message = int(attr['ApproximateNumberOfMessages'])
    num_message_not_visible = int(attr['ApproximateNumberOfMessagesNotVisible'])
    queue_value = sum([num_message, num_message_not_visible])
    sum_msg = """'ApproximateNumberOfMessages' and 'ApproximateNumberOfMessagesNotVisible' = *** [%s] *** for QUEUE NAME: [%s]""" %\
         (queue_value, queue_name)
    return queue_value

def delete_sqs_msg(queue_name, receipt_handle):

    sqs_client = sqs_connection()
    try:
        queue_url = sqs_client.get_queue_url(QueueName=queue_name)["QueueUrl"]
        delete_log_msg = "Deleting msg with ReceiptHandle %s" % receipt_handle
        response = sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    except botocore.exceptions.ClientError as error:
        exception_msg = "FAILURE TO DELETE SQS MSG: Queue Name [%s] with error: [%s]" %\
            (queue_name, error)
        return None

    delete_log_msg_resp = "Response from delete from queue: %s" % response
    return response

### S3 ###
def write_s3(row, bucket, name, dates):
    """Write S3 Bucket"""
    
    s3_resource = boto3.resource('s3')
    #obj = s3_resource.get_object(Bucket='bucket', Key='btc.csv')
    #btc = pd.read_csv(io.BytesIO(obj['Body'].read()))
    
    #final = pd.merge(btc, row, on = 'date')
    filename = name + '_' + dates[0] + '.csv'
    csv_buffer = StringIO()
    row.to_csv(csv_buffer)
    
    res = s3_resource.Object(bucket, filename).\
        put(Body=csv_buffer.getvalue())

def row_to_df(dates, prices):
    finalList = []
    for i in range(len(dates)):
        element = [dates[i], prices[i]]
        finalList.append(element)
        pass
    df = pd.DataFrame(finalList, columns = ['date','price'])
    return df
    
def lambda_handler(event, context):
    """Entry Point for Lambda"""
    
    receipt_handle  = event['Records'][0]['receiptHandle'] #sqs message
    #'eventSourceARN': 'arn:aws:sqs:us-east-1:561744971673:producer'
    event_source_arn = event['Records'][0]['eventSourceARN']

    dateList = []
    priceList = []
    
    #s3 = boto3.client('s3')
    #obj = s3.get_object(Bucket='bucket', Key='key')
    #df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    
    # Process Queue
    for record in event['Records']:
        body = json.loads(record['body'])
        dateList.append(str(body['date']))
        priceList.append(body['price'])

        extra_logging = {"body": body, "date": body['date'], "price": body['price']}
        qname = event_source_arn.split(":")[-1]
        extra_logging["queue"] = qname
        res = delete_sqs_msg(queue_name=qname, receipt_handle=receipt_handle)
    
    df = row_to_df(dateList, priceList)
    write_s3(row = df, bucket = 'ids706', name = 'new', dates = dateList)