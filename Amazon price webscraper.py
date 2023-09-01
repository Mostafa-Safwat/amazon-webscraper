import requests
import time
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from pymongo import MongoClient

load_dotenv()
mongo_uri = os.environ.get('MONGO_URI')

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client["mydatabase"]
collection = db["prices"]

url = input('Enter the URL of the product you want to track: ').replace("amazon.eg", "amazon.eg/-/en")
def webscrape():
    try:
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'}
        page = requests.get(url, headers=headers)
        print(page.status_code)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find(id="productTitle").get_text().strip()
        price = soup.find(class_="a-price-whole").get_text().replace(",", "").replace(".", "")
        currency = soup.find(class_="a-price-symbol").get_text()
        price = float(price)

        asin = ""
        for path in url.split("/"):
            if path.startswith("B0"):
                asin = path.split("?")[0]

        old_product = collection.find_one({"asin": asin})
        if(not old_product):
            collection.insert_one({"title": title, "price": price, "currency": currency, "asin": asin})
        else:
            collection.update_one({"asin": asin}, {"$set": {"price": price, "currency": currency}})
        old_price = old_product["price"]
        if price < old_price:
            print(f"Price of {title} has changed to: {currency} {str(price)}")
        else:
            print(f"Price of {title} has not changed: {str(price)}")
    except:
        print("Error: Could not retrieve price. Retrying in 5 seconds...")
        time.sleep(5)
        webscrape()
webscrape()

