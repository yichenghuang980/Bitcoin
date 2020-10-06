# Bitcoin Price Prediction

## Basic Work Flow
This program is intended to build a serverless data engineering pipeline and fit a linear regression model
to predict Bitcoin price. 
First, It will scrape data from specific websites once a day and update the corresponding S3 bucket.
Next, trigger the producer lambda and ask SQS to perform extractions of data.
Afterwards, trigger the consumer lambda and interaction with SQS again to get data.
Lastly, connect with AWS SageMaker and fit a linear regression model and predict Bitcoin price next day.

## Tools and Services involved
The following aws services are included:
1. CloudWatch
2. Lambda
3. DynamoDB
4. SQS
5. AWS SageMaker API
