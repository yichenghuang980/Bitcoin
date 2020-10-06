import click
import requests
from bs4 import BeautifulSoup

@click.command()
@click.option('--url')
def scrape(url):
    html_content = requests.get(url)
    try:
        html_content.raise_for_status()
        pass
    except Exception as e:
        print('Unable to access web page')
        return
    
    soup = BeautifulSoup(html_content.text, "lxml")
    print(soup.title.text)
    
    btc_table = soup.find('table', attrs = {'class': 'styled-table full-size-table'})
    btc_data = btc_table.tbody.find_all("tr")
    header = (btc_data[0].find_all("th"))
    
    headings = []
    for td in btc_data[0].find_all("th"):
        # remove any newlines and extra spaces
        headings.append(td.text.replace('\n', ' ').strip())
        print(headings)
        pass
    
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

    print(table_data)


if __name__ == '__main__':
    scrape()