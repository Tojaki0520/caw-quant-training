import requests
import pandas as pd

# Read url
payload = {'fsym': 'BTC', 
           'tsym': 'USDT', 
           'start_time': '2017-04-01', 
           'end_time': '2020-04-01', 
           'e': 'binance'}
r = requests.get('https://min-api.cryptocompare.com/data/v2/histohour', params=payload)
# Construct DataFrame
data = r.json().get('Data').get('Data')
df = pd.DataFrame(data)
# Manipulate Columns
columns = ['close', 'high', 'low', 'open', 'volume', 'baseVolume', 'datetime']
df['volume'] = df['volumeto'] - df['volumefrom']
df['baseVolume'] = df['volumefrom']
df['datetime'] = pd.to_datetime(df['time'],unit='s')
df = df[columns]
# Output csv
df.to_csv('BTC_USDT_1h_Test.csv',index=False)