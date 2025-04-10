import requests
from bs4 import BeautifulSoup

import psycopg2

conn = psycopg2.connect(
    dbname='pythonscraping_db',
    user='postgres',
    password=1,
    host='localhost',
    port='5439')
curs = conn.cursor()

HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "accept-language": "en-US,en;q=0.9,ru;q=0.8,fr-FR;q=0.7,fr;q=0.6,uz;q=0.5",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd", }

website_url = 'https://www.axcapital.ae/rent/dubai/properties-for-rent'
try:
    response = requests.get(website_url, headers=HEADERS)
    print(website_url)

    soup = BeautifulSoup(response.content, "html.parser")
    property_locations = soup.find_all(class_='relative flex w-full flex-grow flex-col px-6 py-4 pt-6')

    for location in property_locations:
        location_element = location.find(class_='mb-1 flex items-center text-white')
        if location_element:
            location_text = location_element.getText(strip=True)
            print('Location:', location_text)
            curs.execute("insert into properties (location) values (%s)", (location_text,))
        else:
            print('Location element not found.')
    conn.commit()
    print('locations were stored into database')

except requests.RequestException as e:
    print(f"Request error: {e}")
except psycopg2.Error as e:
    print(f"Database error: {e}")
finally:
    if curs:
        curs.close()
    if conn:
        conn.close()

curs.close()
conn.close()
