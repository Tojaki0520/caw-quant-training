import requests
import pandas as pd
import time
from datetime import datetime
from datetime import timedelta

# Optional
# Class for CryptoCompare
class CryptoCompare:
    def __init__(self):
        self.payload = {}

    def get_candle_helper(self, fsym, tsym, freq, limit, toTs, e):
        # Read url
        self.payload = {'fsym': fsym, 
                        'tsym': tsym, 
                        'aggregate': freq,
                        'aggregatePredictableTimePeriods': 'false',
                        'limit': limit, 
                        'toTs': toTs, 
                        'e': e}
        r = requests.get('https://min-api.cryptocompare.com/data/v2/histohour', params=payload)
        # Construct DataFrame
        data = r.json().get('Data').get('Data')
        df = pd.DataFrame(data)
        # Manipulate Columns
        columns = ['close', 'high', 'low', 'open', 'volume', 'baseVolume', 'datetime']
        df['volume'] = df['volumefrom']
        df['baseVolume'] = df['volumeto']
        df['datetime'] = pd.to_datetime(df['time'],unit='s')
        df = df[columns]
        df[['close', 'high', 'low', 'open', 'volume', 'baseVolume']] = df[['close', 'high', 'low', 'open', 'volume', 'baseVolume']].astype(float)
        return df

    # Task 1
    def get_candle(self, fsym, tsym, freq, start_time, end_time, e):
        # Time variable
        start_datetime = datetime.strptime(start_time, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_time, '%Y-%m-%d')
        total_limit = (end_datetime - start_datetime).days
        total_limit -= 1
        curr_datetime = start_datetime + timedelta(hours = 24)
        unix = time.mktime(curr_datetime.timetuple())
        # Helper function
        df = self.get_candle_helper(fsym, tsym, freq, '24', unix, e)
        # Output csv
        df.to_csv('BTC_USDT_1h_Test.csv',index=False)
        # Loop to the beginning
        while total_limit>0:
            start_datetime = curr_datetime
            total_limit -= 1
            curr_datetime = start_datetime + timedelta(hours = 24)
            unix = time.mktime(curr_datetime.timetuple())
            # Helper function
            df = self.get_candle_helper(fsym, tsym, freq, '23', unix, e)
            # Output csv
            df.to_csv('BTC_USDT_1h_Test.csv', mode='a', index=False, header=False)

    # Optional
    # Member function for TOPLIST endpoint
    def get_toplist(self, limit, page, tsym):
        # Read url
        self.payload = {'tsym': tsym, 
                   'limit': limit, 
                   'page': page}
        r = requests.get('https://min-api.cryptocompare.com/data/top/mktcapfull', params=payload)
        # Construct DataFrame
        data = r.json().get('Data')
        coin_data = []
        for d in data:
            coin_data.append(d.get('CoinInfo'))
        df = pd.DataFrame(coin_data)
        # Manipulate Columns
        columns = ['Id', 'Name', 'Algorithm', 'BlockNumber', 'BlockTime', 'BlockReward']
        df = df[columns]
        # Output csv
        df.to_csv('TOPLIST_USDT.csv',index=False)