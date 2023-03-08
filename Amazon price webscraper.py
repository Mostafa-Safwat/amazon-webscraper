#Important imports
import requests
from bs4 import BeautifulSoup
#Amazon product url
url = 'https://www.amazon.eg/-/en/LG-Dis-27GN650-UltraGear-Gaming/dp/B08VRPGMKP/ref=sr_1_1?crid=2OCN4XABMHFKW&keywords=LG+27GN650-B&qid=1661272068&sprefix=lg+27gn650-b%2Caps%2C130&sr=8-1'
#Paste your user agent here by searching "my user agent" on google.
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
title = soup.find(id="productTitle").get_text() #Use inspect on a webpage and find the product title if needed.
price = soup.find(class_="a-price-whole").get_text() #Change class_ to id if needed. Add the amazon id/class for the product price.
price = price.replace(",", "")
price = float(price)
if(price < 7500): #Checking price. Change the number to your target price for the product.
 print("Price has changed to: " + str(price))
else:
 print("Price has not changed: " + str(price))