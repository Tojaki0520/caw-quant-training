from binance.client import Client
import pandas as pd

# Setup trading api
api_key = open("task2_api.txt", "r").read()
api_secret = 'HuCf5afQWv8eRbiLXRCmTkYXOLEF3WCen5iWdd7YI8y6tjUz5VbUIfXezNjAS5L9'
client = Client(api_key, api_secret)

# Get candle data(aka kline, histo)
klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
df = pd.DataFrame(klines)
columns = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime',
           'QuoteVolume', 'NumberTrades', 'BaseVolumne', 'QuoteVolumne', 'Ignored']
df.columns = columns
df['OpenTime'] = pd.to_datetime(df['OpenTime'],unit='ms')
df['CloseTime'] = pd.to_datetime(df['CloseTime'],unit='ms')
df.to_csv('klines_data.csv',index=False)

# Get transactions(aka trades)
agg_trades = client.aggregate_trade_iter(symbol='ETHBTC', start_str='30 minutes ago UTC')
agg_trade_list = list(agg_trades)
df2 = pd.DataFrame(agg_trade_list)
trade_columns = ['BestPriceMatch', 'Time', 'Id', 'FirstId', 'LastId', 'BuyerMaker', 'Price', 'Quantity']
df2.columns = trade_columns
df2['Time'] = pd.to_datetime(df2['Time'],unit='ms')
df2.to_csv('trades_data.csv',index=False)

# Get market depth(aka orderbook)
depth = client.get_order_book(symbol='BNBBTC')
df3 = pd.DataFrame(depth)
df3[['bids_PRICE','bids_QTY']] = pd.DataFrame(df3.bids.tolist(), index= df3.index)
df3[['asks_PRICE','asks_QTY']] = pd.DataFrame(df3.asks.tolist(), index= df3.index)
df3 = df3[['lastUpdateId','bids_PRICE','bids_QTY','asks_PRICE','asks_QTY']]
df3.to_csv('depth_data.csv',index=False)

# Optional: Create a test order
order = client.create_test_order(
    symbol='BNBBTC',
    side=Client.SIDE_BUY,
    type=Client.ORDER_TYPE_MARKET,
    quantity=100)
