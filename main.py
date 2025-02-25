import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_ebay(searchquery, num_pages=1):
    url = 'https://www.ebay.com/sch/i.html?_nkw='
    products = []

    for page in range(1, num_pages+1):
        search_url = f'{url}{searchquery}&_pgn={page}'
        response = requests.get(search_url)

        if response.status_code != 200:
            print(f'Error: Failed to retrieve page {page}. Status code: {response.status_code}')
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='s-item__info')

        for item in items:
            title = item.find('div', class_='s-item__title').text.strip()
            price = item.find('span', class_='s-item__price').text.strip()
            link = item.find('a', class_='s-item__link')['href']

            products.append({
                'title': title,
                'price': price,
                'link': link
            })

            print(f'Title: {title}\n - Price: {price}\n - Link: {link}\n')
        
        time.sleep(1)

    return products

search_query = "car"

products = scrape_ebay(search_query, num_pages=3)
df = pd.DataFrame(products)

# filter out shop on ebay ad
df = df[df['title'] != 'Shop on eBay']

df.to_csv('ebay_cars.csv', index=False)