import requests
import time
from bs4 import BeautifulSoup

url = 'https://www.amazon.eg/-/en/LG-Dis-27GN650-UltraGear-Gaming/dp/B08VRPGMKP/ref=sr_1_1?crid=2OCN4XABMHFKW&keywords=LG+27GN650-B&qid=1661272068&sprefix=lg+27gn650-b%2Caps%2C130&sr=8-1'
def webscrape():
    try:
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find(id="productTitle").get_text()
        price = soup.find(class_="a-price-whole").get_text().replace(",", "")
        currency = soup.find(class_="a-price-symbol").get_text()
        price = float(price)
        if(price < 7500):
            print(f"Price of {title.strip()} has changed to: {currency} {str(price)}")
        else:
            print(f"Price has not changed: {str(price)}")
    except:
        print("Error: Could not retrieve price. Retrying in 5 seconds...")
        time.sleep(5)
        webscrape()
webscrape()