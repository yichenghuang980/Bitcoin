from decimal import Rounded
import json
import boto3
import pandas as pd


dynamodb = boto3.resource('dynamodb')

def convert(filename):
    data = pd.read_csv("btc.csv")
    listOfDict = []
    for index, row in data.iterrows():
        newDict = {'Date':'','Price':''}
        newDict['Date'] = row['Date']
        newDict['Price'] = row['Close']
        listOfDict.append(newDict)
        pass
    return listOfDict

def load(bitcoin, dynamodb):
    table = dynamodb.Table('bitcoin')
    
    for i in range(len(bitcoin)):
        response = table.put_item(
            Item={
                'date': bitcoin[i]['Date'],
                'name': "Bitcoin",
                'price': Rounded(bitcoin[i]['Price'])
            }
        )

if __name__ == '__main__':
    load(convert("btc.csv"), dynamodb)