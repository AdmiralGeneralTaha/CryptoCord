import requests
from replit import db

def getCryptoPricesGBP(crypto):
  URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=gbp"
  r = requests.get(url=URL)
  data = r.json()
 
  for i in range(len(data)):
    db[data[i]["id"]] = data[i]["current_price"]

def getCryptoPricesUSD(crypto):
  URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
  r = requests.get(url=URL)
  data = r.json()
 
  for i in range(len(data)):
    db[data[i]["id"]] = data[i]["current_price"]

def getCryptoPricesEUR(crypto):
  URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur"
  r = requests.get(url=URL)
  data = r.json()
 
  for i in range(len(data)):
    db[data[i]["id"]] = data[i]["current_price"]