# Bitcoin Price Prediction

## Demo on Youtube
[![](http://img.youtube.com/vi/BXOnH-wZqGg/0.jpg)](http://www.youtube.com/watch?v=BXOnH-wZqGg "Data Engineering Pipeline")

## Introduction
This repository contains code on building a serverless data engineering pipeline and fit a machine learning model to predict Bitcoin price.

It consists of two parts:
### Part 1: Lambda
It contains two sets of lambda function, .Price and .Text.

producerPrice: triggered by CloudWatch presumably once a day to scrape the specific website, merge into DynamoDB to ensure uniqueness, and then send to SQS instance "producer".

consumerPrice: triggered by EventWatch inside SQS instance "producer" to receive and rearrange messages into a dataframe and save as csv file into S3 bucket "ids706"

producerText: triggered by CloudWatch presumably every 10 - 20 mins to scrape the specific Bitcoin community, merge into DynamoDB to ensure uniqueness, and then send to SQS instance "sentiment".

consumerPrice: triggered by EventWatch inside SQS instance "sentiment" to receive and rearrange messages into a dataframe, interact with AWS Comprehend, and save the final sentiment analyses as .csv file into S3 bucket "ids706"
### Part 2: SageMaker
Import accumulated datasets from a certain period of web scraping and train a machine learning model to predict Bitcoin price.

## Complete Basic Work Flow
First, producer lambda is trigger by CloudWatch and will scrape Bitcoin price once a day and community review every 10-20 mins from specific websites and update the corresponding DynamoDB tables and S3 buckets.

Next, producer lambda function extracts data from DynamoDB and sends messages to SQS.

Afterwards, consumer lambda function is triggered by the EventWatch and transforms messages from SQS queues.

Then, interact with AWS Comprehend to gain sentment analyses.

Lastly, connect with AWS S3 bucket and export data as .csv into it.

Train the SageMaker Machine Learning model with accumulated data and gain prediction.

## Tools and Services involved
The following aws services are included:
1. CloudWatch
2. EventWatch
3. Lambda
4. DynamoDB
5. SQS
6. Comprehend
7. SageMaker
8. S3

## Note
To determine the rate for CloudWatch and save unnecessary computation power, a careful
examination on the community/webiste vitality is required.
The main metric is the average time age between two reviews or comments.

Ideally, keep the CloudWatch for producer lambda function enabled to accumulate datasets.
However, if not training models with the datasets, keep the EventWatch disabled to save storage and computing power.

## Website URL links
Bitcoin price:

https://coincodex.com/crypto/bitcoin/historical-data/
https://coinmarketcap.com/currencies/bitcoin/historical-data/

US Dollar Index:

https://www.marketwatch.com/investing/index/dxy

Standard Poor 500 Index:

https://www.marketwatch.com/investing/index/spx

Ethereum Price:

https://coinmarketcap.com/currencies/ethereum/historical-data/

Bitcoin Community Reviews:

https://www.trustpilot.com/review/bitcoin.com
https://www.investing.com/crypto/bitcoin/chat
