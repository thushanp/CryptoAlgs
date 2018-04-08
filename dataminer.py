import httpRequester
import json
import time
from datetime import datetime

QUERY_TIME_SLEEP = 0

def getAllTradeHistory(currencyPair, maxIter = 10000000000):
    ret = []
    #get current ticker point
    response=httpRequester.sendGetRequest("https://api.bitflyer.jp/v1/executions?symbol="+currencyPair)
    data = json.loads(response)
    beforeID = int(data[0]["id"])
    stillMore=True
    currentIter=0
    while stillMore and currentIter < maxIter:
        currentIter = currentIter+1
        print(beforeID, currentIter)
        response=httpRequester.sendGetRequest("https://api.bitflyer.jp/v1/executions?symbol="+currencyPair+"&before="+str(beforeID)+"&count=100000")
        try:
            data = json.loads(response)
            if len(data)==0:
                stillMore=False
            for entry in data:
                entryData = entry
                date_ms_str = entryData["exec_date"]
                try:
                    datetime_object = datetime.strptime(date_ms_str, '%Y-%m-%dT%H:%M:%S.%f')
                except:
                    #inconsistent formatting issues
                    datetime_object = datetime.strptime(date_ms_str, '%Y-%m-%dT%H:%M:%S')
                date_ms=(datetime_object-datetime_object.utcfromtimestamp(0)).total_seconds()*1000.0
                amount = float(entryData["size"])
                price = float(entryData["price"])
                tradeType = entryData["side"]
                isSell = True
                if tradeType == "BUY":
                    isSell = False
                ret.append([date_ms,price,amount,isSell])
                beforeID = int(entryData["id"])
            time.sleep(QUERY_TIME_SLEEP)
        except:
            #sometimes api's occasionally return bad responses, throws an exception
            print("parsing error when trying to fetch data. Current time "+str(date_ms))
    return sorted(ret,key=lambda x: x[0])
        
def getCurrencyPairs():
    #sometimes exchanges will have an api call to get all pairs -- sometimes not
    response=httpRequester.sendGetRequest("https://api.bitflyer.jp/v1/getmarkets")
    data = json.loads(response)
    ret=[]
    for entry in data:
        ret.append(entry["product_code"])
    return ret

#print function for testing
#print(getAllTradeHistory("btc_jpy",maxIter=3))