from decimal import Decimal
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
        newDict['Price'] = Decimal(row['Close'])
        listOfDict.append(newDict)
        pass
    return listOfDict

def load(bitcoin, dynamodb):
   
    table = dynamodb.Table('bitcoin')
    for entry in bitcoin:
        date = entry['Date']
        price = entry['Price']
        print("Adding date:", date, price)
        table.put_item(Item=entry)

if __name__ == '__main__':
    load(convert("btc.csv"), dynamodb)