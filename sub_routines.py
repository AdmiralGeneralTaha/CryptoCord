import requests
from replit import db

def getCryptoPrices(currency):
  if currency == "£":
    URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=gbp"
  elif currency == "$":
    URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
  else:
    URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur"

  r = requests.get(URL)
  data = r.json()
 
  for i in range(len(data)):
    db[data[i]["id"]] = data[i]["current_price"]

def stdform_convert(price): 
  price, float_point = price.split("e") 
  price = float(price)
  if float_point[0] == "-":
    places_to_move = int(float_point[float_point.rfind("0") + 1])
    for i in range(places_to_move):
      			price /= 10 
  elif float_point[0] == "+":
    places_to_move = int(float_point[float_point.rfind("0") + 1])
    for i in range(places_to_move):
      price *= 10
  return "{:.11f}".format(price)
