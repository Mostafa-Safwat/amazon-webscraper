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

url = input('Enter the URL of the product you want to track: ')
def webscrape():
    try:
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find(id="productTitle").get_text()
        price = soup.find(class_="a-price-whole").get_text().replace(",", "")
        currency = soup.find(class_="a-price-symbol").get_text()
        price = float(price)
        collection.insert_one({"prices": price})
        if price < 30000:
            print(f"Price of {title.strip()} has changed to: {currency} {str(price)}")
        else:
            print(f"Price has not changed: {str(price)}")
    except:
        print("Error: Could not retrieve price. Retrying in 5 seconds...")
        time.sleep(5)
        webscrape()
webscrape()