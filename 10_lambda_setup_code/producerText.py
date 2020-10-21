import boto3
import json
import sys
import os
import requests
import datetime
import re
import bs4 as BeautifulSoup

DYNAMODB = boto3.resource('dynamodb')
TABLE = DYNAMODB.Table("demoComment")
QUEUE = "sentiment"
SQS = boto3.client("sqs")

# SETUP LOGGING
import logging
from pythonjsonlogger import jsonlogger

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
LOG.addHandler(logHandler)

def scan_table(table):
    """Scans table and return results"""

    LOG.info(f"Scanning Table {table}")
    
    response = table.scan()
    items = response['Items']
    LOG.info(f"Found {len(items)} Items")
    return items[0:6]

def send_sqs_msg(msg, queue_name, delay=0):
    """Send SQS Message

    Expects an SQS queue_name and msg in a dictionary format.
    Returns a response dictionary. 
    """
    queue_url = SQS.get_queue_url(QueueName=queue_name)["QueueUrl"]
    queue_send_log_msg = "Send message to queue url: %s, with body: %s" %\
        (queue_url, msg)
    LOG.info(queue_send_log_msg)
    
    json_msg = json.dumps(msg)
    response = SQS.send_message(
        QueueUrl=queue_url,
        MessageBody=json_msg,
        DelaySeconds=delay)
    queue_send_log_msg_resp = "Message Response: %s for queue url: %s" %\
        (response, queue_url) 
    LOG.info(queue_send_log_msg_resp)
    return response

def send_emissions(table, queue_name):
    """Send Emissions"""

    items = scan_table(table=table)
    for item in items:
        LOG.info(f"Sending item {item} to queue: {queue_name}")
        response = send_sqs_msg(item, queue_name=queue_name)
        LOG.debug(response)
        
def scrape(url, table):
    
    html_content = requests.get(url)
    html_content.raise_for_status() 
    soup = BeautifulSoup(html_content.content, "lxml")
    com_data = soup.find('div', attrs = {'class': 'review-list'})
    review_dates = com_data.find_all('div', attrs = {'class': 'review-content-header__dates'})
    review_date = review_dates[0].find('script').string
    jsonObj = json.loads(review_date)
    date = datetime.datetime.strptime(jsonObj['publishedDate'],"%Y-%m-%dT%H:%M:%SZ")
    
    review_cards = com_data.find_all('div', attrs = {'class': 'review-content__body'})
    new = review_cards[0].text.strip().lstrip().replace('\n', '')
    
    response = table.put_item(
    Item={
        'date': str(date.strftime('%Y-%m-%d %H:%M:%S')),
        'body': new
    }
    )

def lambda_handler(event, context):
   
    extra_logging = {"table": TABLE, "queue": QUEUE}
    LOG.info(f"event {event}, context {context}", extra=extra_logging)
    scrape('https://www.trustpilot.com/review/bitcoin.com', TABLE)
    send_emissions(table=TABLE, queue_name=QUEUE)
    