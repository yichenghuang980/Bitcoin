import pandas as pd
import numpy as np

btc = pd.read_csv('Datasets/btc.csv').rename({'Price': 'btcPrice'}, axis = 1)
btc['Date'] = pd.to_datetime(btc['Date'])

eth = pd.read_csv('Datasets/eth.csv')[['Date', 'Close']].rename({'Close': 'ethPrice'}, axis = 1)
eth['Date'] = pd.to_datetime(eth['Date'])

dollar = pd.read_csv('Datasets/dollar.csv')[['Date', 'Price']].rename({'Price': 'dollarIndex'}, axis = 1)
dollar['Date'] = pd.to_datetime(dollar['Date'])

sp = pd.read_csv('Datasets/sp.csv')[['Date', 'Adj Close']].rename({'Adj Close': 'spIndex'}, axis = 1)
sp['Date'] = pd.to_datetime(sp['Date'])

sentiment = pd.read_csv('Datasets/sentiment.csv')
sentiment['datetime'] = pd.to_datetime(sentiment['datetime'])
sentiment['datetime'] = sentiment['datetime'].dt.date
sentiment = sentiment.groupby('datetime', as_index = False).agg(lambda x:x.value_counts().index[0])
sentiment['Sentiment'] = sentiment['Sentiment'].astype('str')
sentiment['datetime'] = sentiment['datetime'].astype('str')

# merge bitcoin and ethereum
crypto = pd.merge(btc, eth, on = 'Date', validate = '1:1', indicator = True)
crypto['_merge'].value_counts()
crypto.drop('_merge', axis = 1, inplace = True)

# merge dollar
includeDollar = pd.merge(crypto, dollar, on = 'Date', validate = '1:1', indicator = True)
includeDollar['_merge'].value_counts()
includeDollar.drop('_merge', axis = 1, inplace = True)

# merge sp index
includeSp = pd.merge(includeDollar, sp, on = 'Date', validate = '1:1', indicator = True)
includeSp['_merge'].value_counts()
includeSp.drop('_merge', axis = 1, inplace = True)

# merge sentiment
includeSp['Date'] = includeSp['Date'].astype('str')
final = pd.merge(includeSp, sentiment, left_on = 'Date', right_on = 'datetime', validate = '1:1', indicator = True)
final._merge.value_counts()
final.drop(['_merge', 'datetime'], axis = 1, inplace = True)
