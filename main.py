import requests
from bs4 import BeautifulSoup

import psycopg2

conn = psycopg2.connect(
    dbname='pythonscraping_db',
    user='postgres',
    password=1,
    host='localhost',
    port='5439'
)
curs = conn.cursor()

data_url = requests.get('https://www.axcapital.ae/rent/dubai/properties-for-rent')

soup = BeautifulSoup(data_url.text, 'lxml')
data_request = soup.find_all(class_='properties')

for data in data_request:
    text=data.getText(strip=True)
    curs.execute("insert into properties (data) values (%s)", (text,))

conn.commit()
curs.close()
conn.close()

print(data_request)
