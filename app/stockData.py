from datetime import date
from urllib.request import urlopen
import json
import tweepy


def getYesterdayDate():

    dayToConvert = today.day
    yesterday = str(int(dayToConvert) - 1)

    if(len(yesterday) == 2):
        return yesterday
    else:
        return "0", yesterday


def calculateStockDifference(stockX, stockY):

    if(stockX == stockY):
        return "0%"
    
    elif(stockX < stockY):
        return "Down " + str(1.0 - (stockX/stockY)) + "%"
    else:
        return "Up " + str(1.0 - (stockY/stockX)) + "%"


ownedStocks = [("2B76.DE", "iShares Automation & Robotics UCITS ETF USD"),
 ("ZPRV.DE", "SPDR MSCI USA Small Cap Value Weighted UCITS ETF"),
  ("DXET.DE", "Xtrackers Euro STOXX 50 UCITS ETF 1C")]

#today = date.today() # real
#yesterday = getYesterdayDate() # real
today = "2019-12-23" # placeholder
yesterday = "2019-12-20" # placeholder

for i in range(len(ownedStocks)):
    
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + ownedStocks[i][0] + "&interval=60min&apikey=0OUANH47LJMGA7JA&datatype=json"
    
    with urlopen(url) as response:
        source = response.read()
    
    data = json.loads(source)

    #todayValue = data["Time Series (60min)"][str(today.year) + "-" + str(today.month) + "-" + str(today.day) + " 08:00:00"]["1. open"] #real
    todayValue = data["Time Series (60min)"][today + " 09:00:00"]["1. open"] #placeholder for testing
    #yesterdayValue = data["Time Series (60min)"][str(yesterday.year) + "-" + str(yesterday.month) + "-" + str(yesterday.day) + " 08:00:00"]["1. open"] # real
    yesterdayValue = data["Time Series (60min)"][yesterday + " 03:00:00"]["1. open"] #placeholder for testing

    tupleAsList = list(ownedStocks[i])

    tupleAsList.append(todayValue)
    tupleAsList.append(yesterdayValue)
    tupleAsList.append(calculateStockDifference(float(todayValue), float(yesterdayValue)))

    ownedStocks[i] = tuple(tupleAsList)

    

    #print(ownedStocks[i][1], "----------------------------------------------------------------\n")
    #print(json.dumps(data, indent=2))
print(ownedStocks)


