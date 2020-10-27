import boto3
import requests
from bs4 import BeautifulSoup
import random

def demo(url, dynamodb, table):
    html_content = requests.get()
    html_content.raise_for_status()
    
    soup = BeautifulSoup(html_content.text, "lxml")
    
    btc_table = soup.find('table', attrs = {'class': 'styled-table full-size-table'})
    btc_data = btc_table.tbody.find_all("tr")
    header = (btc_data[0].find_all("th"))
    
    headings = []
    for td in btc_data[0].find_all("th"):
        # remove any newlines and extra spaces
        headings.append(td.text.replace('\n', ' ').strip())
    
    data = {}
    # Get all the rows
    table_data = []
    for tr in btc_table.tbody.find_all("tr"): # find all tr's from table's tbody
        t_row = {}
        # t_row = {'Date': '', 'Open': '', 'High': '', 'Close': '', 'Volume': '', 'Market Cap': ''}

        # find all td's(6) in tr and zip it with t_header
        for td, th in zip(tr.find_all("td"), headings): 
            t_row[th] = td.text.replace('\n', '').strip().replace('$\u202f','')
        table_data.append(t_row)
        pass
    table_data.pop(0)
    
    index = random.randint(0, len(table_data))
    response = table.put_item(
        Item={
            'date': table_data[index]['Date'],
            'name': "Bitcoin",
            'price': table_data[index]['Close']
        }
    )
    
    return table_data[index]
    
if __name__ == '__main__':
    demo("https://coincodex.com/crypto/bitcoin/historical-data/", boto3.resource('dynamodb'), boto3.resource('dynamodb').Table("bitcoin"))