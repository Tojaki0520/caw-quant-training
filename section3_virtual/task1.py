from binance.websockets import BinanceSocketManager
from binance.client import Client
from binance.enums import *
import pandas as pd
import csv
from datetime import datetime  # For datetime objects
import math

def process_message(msg):
    print("message type: {}".format(msg['e']))
    print(msg)
    # do something
    row = [round(float(msg['k']['c']),2),round(float(msg['k']['h']),2),round(float(msg['k']['l']),2),
           round(float(msg['k']['o']),2),round(float(msg['k']['Q']),4),round(float(msg['k']['v']),2),
           datetime.fromtimestamp(int(float(msg['E'])/1000))]
    b = open('./result.csv', 'a', newline='')
    #b = open('./log/BTC_USDT_1h_SMACross.csv', 'a', newline='')
    a = csv.writer(b)
    a.writerow(row)
    b.close()


# Setup trading api
api_key = open("task1_api.txt", "r").read()
api_secret = 'HuCf5afQWv8eRbiLXRCmTkYXOLEF3WCen5iWdd7YI8y6tjUz5VbUIfXezNjAS5L9'
client = Client(api_key, api_secret)

column_names = ['close','high','low','open','volume','baseVolume','datetime']
b = open('./result.csv', 'a', newline='')
#b = open('./log/BTC_USDT_1h_SMACross.csv', 'a', newline='')
a = csv.writer(b)
a.writerow(column_names)
b.close()

bm = BinanceSocketManager(client)
# start any sockets here, i.e a trade socket
conn_key = bm.start_kline_socket('BTCUSDT', process_message, interval=KLINE_INTERVAL_1MINUTE)
# then start the socket manager
bm.start()

