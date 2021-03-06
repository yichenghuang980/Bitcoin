import json
import boto3
import pandas as pd
from smart_open import smart_open

DYNAMODB = boto3.resource('dynamodb')
s3 = boto3.resource('s3')
bucket = s3.Bucket('ids706')
data_key = 'bitcoin_reddit_all.csv.zip'
data_location = 's3://{}/{}'.format(bucket.name, data_key)
    
def convert(filename):
    
    final = pd.read_csv(filename, low_memory = False)
    
    listOfDict = []
    
    for index, row in final.iterrows():
        newDict = {'time':'','body':''}
        newDict['Date'] = row['datetime']
        newDict['text'] = row['body']
        listOfDict.append(newDict)
        pass
    
    return listOfDict

def load(dictName, dynamodb):
    table = dynamodb.Table('demoComment')
    
    for i in range(len(dictName)):
        response = table.put_item(
            Item={
                'datetime': dictName[i]['Date'],
                'body': dictName[i]['text']
            }
        )

if __name__ == '__main__':
    load(convert("sample.csv"), DYNAMODB)