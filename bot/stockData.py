from datetime import date
import datetime
import time
from urllib.request import urlopen
import json
import tweepy
import schedule
import emojis


ownedStocks = [("2B76.DE", "iShares Automation & Robotics UCITS"),
 ("ZPRV.DE", "SPDR MSCI USA Small Cap Value Weighted UCITS"),
  ("DXET.DE", "Xtrackers Euro STOXX 50 UCITS"), ("IS3N.DE", "iShares Core MSCI EM IMI UCITS"),
   ("SXR8.DE","iShares Core S&P 500 UCITS"), ("QDVR.DE", "iShares MSCI USA SRI UCITS"), ("SPYX.DE", "SPDR MSCI Emerging Markets Small Cap UCITS"), 
    ("ZPRX.DE", "SPDR MSCI Europe Small Cap Value Weighted UCITS")]

toBeTweeted = []

def main():

    if date.today().weekday() == 0:
        day_jump = 3
    else:
        day_jump = 1
    
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days = day_jump)

    counter = 0
    pointer1 = 0
    pointer2 = 3

    for i in range(len(ownedStocks)):
        
        counter += 1

        if(counter > 3):
            time.sleep(60)
            counter = 0
            tweet(pointer1, pointer2, False)
            pointer1 += 3
            pointer2 += 3
        
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + ownedStocks[i][0] + "&interval=60min&apikey=YOURKEY&datatype=json"
        
        with urlopen(url) as response:
            source = response.read()
        
        data = json.loads(source)
        
        todayValue = ""
        yesterdayValue = ""
        for j in range(11, 0, -1):
            try:
                todayValue = data["Time Series (60min)"][str(today.year) + "-" + addZero(str(today.month)) + "-" + addZero(str(today.day)) + " " + addZero(str(j)) + ":00:00"]["1. open"]
                yesterdayValue = data["Time Series (60min)"][str(yesterday.year) + "-" + addZero(str(yesterday.month)) + "-" + addZero(str(yesterday.day)) + " " + addZero(str(j)) + ":00:00"]["1. open"]
                if(len(str(todayValue)) > 15 or len(str(yesterdayValue)) > 15):
                    continue
                else:
                    break
            except:
                continue
        

        tupleAsList = list(ownedStocks[i])
        tupleAsList.append(todayValue)
        tupleAsList.append(yesterdayValue)
        tupleAsList.append(calculateStockDifference(float(todayValue), float(yesterdayValue)))

        ownedStocks[i] = tuple(tupleAsList)
    
    tweet(pointer1, -1, True)

def addZero(str):
    if len(str) == 1:
        return "0" + str
    else:
        return str

def getYesterdayDate(today):

    dayToConvert = today.day
    yesterday = str(int(dayToConvert) - 1)

    if(len(yesterday) == 2):
        return yesterday
    else:
        return "0" + yesterday



def calculateStockDifference(stockX, stockY):

    if(stockX == stockY):
        return emojis.encode("stayed the same. :loop:")
    
    elif(stockX < stockY):
        return emojis.encode("gone down " + str(round(((1.0 - (stockX/stockY))*100), 2)) + "%. :chart_with_downwards_trend:")
    else:
        return emojis.encode("gone up " + str(round((1.0 - (stockY/stockX))*100, 2)) + "%. :chart_with_upwards_trend:")



def toString(listOfTuples, firstTweet):

    msg = ""

    if(firstTweet):
        msg = "Daily update:"
    else:
        msg = "..." 

    stringToReturn = "@FransmanLucas\n" + msg + "\n\n"

    for tuple in listOfTuples:
        stringToReturn += "\t" + tuple[1] + " has " + tuple[-1] + "\n\n"

    return stringToReturn



def tweet(index1, index2, sendTweet):
    
    auth = tweepy.OAuthHandler("*******", "********")
    auth.set_access_token("*********", "**********")

    if(index1 == 0):
        firstTweet = True
    else:
        firstTweet = False 

    twitter = tweepy.API(auth)

    try:
        twitter.verify_credentials()
        print("Twitter Authentication OK")
    except:
        print("Error during authentication")

    if(sendTweet):
        toBeTweeted.insert(0, toString(ownedStocks[index1:index2], firstTweet))
        for i in range(len(toBeTweeted)):
            twitter.update_status(toBeTweeted[i])
    else:
        toBeTweeted.insert(0, toString(ownedStocks[index1:index2], firstTweet))



if __name__ == "__main__":
    print("Running...")
    main()





