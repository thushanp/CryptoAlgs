from datetime import datetime
import json
from urllib import urlopen


def getPrice_GDAX(currency):
  url = urlopen("https://api-public.sandbox.gdax.com/products/{symbol}/ticker".format(symbol=currency))
  data = json.loads(url.read())


  print data.get("price")
  return data.get("price")

# getPrice_GDAX('ETH-USD')



