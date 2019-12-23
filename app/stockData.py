from urllib.request import urlopen
import json

ownedStocks = [("2B76.DE", "iShares Automation & Robotics UCITS ETF USD"),
 ("ZPRV.DE", "SPDR MSCI USA Small Cap Value Weighted UCITS ETF"),
  ("DXET.DE", "Xtrackers Euro STOXX 50 UCITS ETF 1C")]


for i in range(len(ownedStocks)):
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + ownedStocks[i][0] + "&interval=60min&apikey=0OUANH47LJMGA7JA&datatype=json"
    with urlopen(url) as response:
        source = response.read()
    
    data = json.loads(source)

    print(ownedStocks[i][1], "--------------------------------------------------------------------------------------------------")
    print(json.dumps(data, indent=2))

