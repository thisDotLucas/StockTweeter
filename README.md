# StockTweeter
A Twitter bot that tweets change in value of my currently owned stocks daily @myTwitterAccount. Bot account: @9000stock.
I runt it daily using AWS EC2.
## How to use
Step 1. Get a free [Alpha Vantage api key](https://www.alphavantage.co/) and insert it into the url, apikey=YOURKEY.

Step 2. Create a Twitter developer account so you can get a API key and access token.

Step 3. Insert into tweepy.OAuthHandler("API key", "secret API key") and into auth.set_access_token("acces token", "secret acces token") 

Step 4. Empty the ownedStocks array and insert your stocks as tuples in the format (Ticker symbol, name of stock).

Step 5. Done, if you want it to run daily you need to run it on a server or schedule it on your computer.
## Example Tweet
![Skärmklipp](https://user-images.githubusercontent.com/43991152/72163556-b61e3780-33cc-11ea-87a6-4227a2ecc97a.PNG)
