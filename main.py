import time
from smartapi import SmartConnect
import datetime

API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
REFRESH_TOKEN = "YOUR_REFRESH_TOKEN"

BUY_QTY = 100
BUY_DROP = 0.05
SELL_PROFIT = 0.10

SYMBOL_TOKEN = "123456"
EXCHANGE = "NSE"

obj = SmartConnect(api_key=API_KEY)

data = obj.generateSession("YOUR_CLIENT_ID", "YOUR_PASSWORD")
feedToken = obj.getfeedToken()

print("Bot started...")

def place_buy(price):
    orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": "NHPC-EQ",
        "symboltoken": SYMBOL_TOKEN,
        "transactiontype": "BUY",
        "exchange": EXCHANGE,
        "ordertype": "LIMIT",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": price,
        "squareoff": 0,
        "stoploss": 0,
        "quantity": BUY_QTY
    }
    try:
        orderId = obj.placeOrder(orderparams)
        print("BUY placed @", price)
        return orderId
    except Exception as e:
        print("Buy Error:", e)

def place_sell(price):
    orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": "NHPC-EQ",
        "symboltoken": SYMBOL_TOKEN,
        "transactiontype": "SELL",
        "exchange": EXCHANGE,
        "ordertype": "LIMIT",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": price,
        "squareoff": 0,
        "stoploss": 0,
        "quantity": BUY_QTY
    }
    try:
        orderId = obj.placeOrder(orderparams)
        print("SELL placed @", price)
        return orderId
    except Exception as e:
        print("Sell Error:", e)

last_buy_price = None

while True:
    try:
        ltp = obj.ltpData(EXCHANGE, "NHPC-EQ", SYMBOL_TOKEN)['data']['ltp']
        print("LTP:", ltp)

        if last_buy_price is None:
            last_buy_price = ltp

        if ltp <= last_buy_price - BUY_DROP:
            place_buy(ltp)
            last_buy_price = ltp

        if ltp >= last_buy_price + SELL_PROFIT:
            place_sell(ltp)
            last_buy_price = ltp

        time.sleep(2)

    except Exception as e:
        print("Loop Error:", e)
        time.sleep(5)
