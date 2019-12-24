from datetime import date
import time
from urllib.request import urlopen
import json
import tweepy
import schedule


ownedStocks = [("2B76.DE", "iShares Automation & Robotics UCITS"),
 ("ZPRV.DE", "SPDR MSCI USA Small Cap Value Weighted UCITS"),
  ("DXET.DE", "Xtrackers Euro STOXX 50 UCITS"), ("IS3N.DE", "iShares Core MSCI EM IMI UCITS"),
   ("SXR8.DE","iShares Core S&P 500 UCITS"), ("QDVR.DE", "iShares MSCI USA SRI UCITS")]


#today = "2019-12-12" # placeholder
#yesterday = "2019-12-11" # placeholder

toBeTweeted = []

def scheduleTweets():
    
    schedule.every().day.at("11:00").do(main)

    while True:
        schedule.run_pending()
        time.sleep(60)
        print("Running...")


def main():

    today = date.today() # real
    yesterday = getYesterdayDate() # real

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
        
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + ownedStocks[i][0] + "&interval=60min&apikey=0OUANH47LJMGA7JA&datatype=json"
        
        with urlopen(url) as response:
            source = response.read()
        
        data = json.loads(source)
        
        for i in range(9):
            todayValue = data["Time Series (60min)"][str(today.year) + "-" + str(today.month) + "-" + str(today.day) + " 0" + i + ":00:00"]["1. open"] #real
            #todayValue = data["Time Series (60min)"][today + " 03:00:00"]["1. open"] #placeholder for testing
            yesterdayValue = data["Time Series (60min)"][str(yesterday.year) + "-" + str(yesterday.month) + "-" + str(yesterday.day) + " 0" + i + ":00:00"]["1. open"] # real
            #yesterdayValue = data["Time Series (60min)"][yesterday + " 03:00:00"]["1. open"] #placeholder for testing

        tupleAsList = list(ownedStocks[i])

        tupleAsList.append(todayValue)
        tupleAsList.append(yesterdayValue)
        tupleAsList.append(calculateStockDifference(float(todayValue), float(yesterdayValue)))

        ownedStocks[i] = tuple(tupleAsList)
    
    tweet(pointer1, -1, True)



def getYesterdayDate():

    dayToConvert = today.day
    yesterday = str(int(dayToConvert) - 1)

    if(len(yesterday) == 2):
        return yesterday
    else:
        return "0", yesterday



def calculateStockDifference(stockX, stockY):

    if(stockX == stockY):
        return "stayed the same."
    
    elif(stockX < stockY):
        return "down " + str(1.0 - (stockX/stockY)) + "%."
    else:
        return "up " + str(1.0 - (stockY/stockX)) + "%."
        print()



def toString(listOfTuples, firstTweet):

    msg = ""

    if(firstTweet):
        msg = "Daily update:"
    else:
        msg = "..." 

    stringToReturn = "@FransmanLucas\n" + msg + "\n\n"

    for tuple in listOfTuples:
        stringToReturn += "\t" + tuple[1] + " has gone " + tuple[-1] + "\n\n"

    return stringToReturn



def tweet(index1, index2, sendTweet):
    
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler("fC0HQpLsKkfO6DJKzsLewsELO", "hdomPuOGsF9htlPoIdMLWFU5ozwC51aFbvCCMRm30ePd6bMTyI")
    auth.set_access_token("1209246142023770112-ftY5YILvSztKb5QWVzuwIeoBoXfvNN", "MRjDG89sEjtsIp81uE8okUoXOV1ItDvLlScBPI0ywYfvV")

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
    scheduleTweets()


