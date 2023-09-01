from flask import Flask, request, jsonify
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

app = Flask(__name__)

@app.route('/price', methods=['POST'])
def get_price():
    url = request.json['url']
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'}
    page = requests.get(url, headers=headers)
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
        old_price = old_product['price']
        if price < old_price:
            collection.update_one({"asin": asin}, {"$set": {"price": price}})
            return jsonify({"message": f"Price of {title} has decreased from {old_price} to {currency} {price}"})
        else:
            return jsonify({"message": f"Price of {title} has not changed: {currency} {price}"})

if __name__ == '__main__':
    app.run(debug=True)