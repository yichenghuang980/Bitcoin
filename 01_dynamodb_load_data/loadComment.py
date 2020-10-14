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
    
    data = pd.read_csv(filename, compression = 'zip', lineterminator='\n', low_memory = False)
    clean = data.drop(['Unnamed: 0', 'subreddit', 'created_utc', 'date', 'author'], axis = 1)
    clean['label'] = 0
    final = pd.DataFrame({})
    final = final.append(clean[clean['score'] > 0].replace(0, 1))
    final = final.append(clean[clean['score'] <= 0])
    final = final.rename(columns = {'Unnamed: 0':'commentID'})
    
    listOfDict = []
    
    for index, row in final.iterrows():
        newDict = {'Id':'','Date':'','body':'','label':''}
        newDict['Id'] = row['commentID']
        newDict['Date'] = row['datetime']
        newDict['text'] = row['body']
        newDict['label'] = row['label']
        listOfDict.append(newDict)
        pass
    return listOfDict

def load(dictName, dynamodb):
    table = dynamodb.Table('comment')
    
    for i in range(len(dictName)):
        response = table.put_item(
            Item={
                'commentID': dictName[i]['Id'],
                'datetime': dictName[i]['Date'],
                'body': dictName[i]['text'],
                'label': int(dictName[i]['label'])
            }
        )

if __name__ == '__main__':
    convert(data_location)