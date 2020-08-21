# all built-in libraries at the top
import os
import datetime

# all third-party libraries in the middle
import backtrader as bt
import pandas as pd
import matplotlib as plt

# all your own modules in the end
from CryptoCompare import CryptoCompare

# params
datadir = './data' # data path
logdir = './log' # log path
reportdir = './report' # report path
datafile = 'BTC_USDT_1h.csv' # data file
logfile = 'BTC_USDT_1h_Test_10_20_2020-01-01_2020-04-01.csv'
figfile = 'BTC_USDT_1h_Test_10_20_2020-01-01_2020-04-01.png'
from_datetime = '2020-01-01 00:00:00' # start time 
to_datetime = '2020-04-01 00:00:00' # end time

# get candle data
"""data_fetcher = CryptoCompare()
data_fetcher.get_candle('BTC', 'USDT', '1', '2017-04-01', '2020-04-01', 'binance')
os.rename('./BTC_USDT_1h.csv','./data/BTC_USDT_1h.csv')"""

# introduce new DonchianChannels indicator
class DonchianChannels(bt.Indicator):
    
    lines = ('high', 'low',)

    # high and low price of 20-day period
    def __init__(self):
        self.l.high = bt.ind.Highest(self.data.high(-1), period=20)
        self.l.low = bt.ind.Lowest(self.data.low(-1), period=20)

# define stategy
class TestStrategy(bt.Strategy):
    def __init__(self):
        # initialize indicator
        self.dc = DonchianChannels()
    
    def next(self):
        # buy
        if not self.position:
            if self.data[0] > self.dc.high[0]:
                self.buy()
        # sell
        elif self.position:
            if self.data[0] < self.dc.low[0]:
                self.sell()

# initialization
cerebro = bt.Cerebro()

# feed data
data = pd.read_csv(
    os.path.join(datadir, datafile), index_col='datetime', parse_dates=True)
data = data.loc[
    (data.index >= pd.to_datetime(from_datetime)) &
    (data.index <= pd.to_datetime(to_datetime))]
datafeed = bt.feeds.PandasData(dataname=data)
cerebro.adddata(datafeed)

# feed strategy
cerebro.addstrategy(TestStrategy)

# additional backtest setting
#cerebro.addsizer(bt.sizers.PercentSizer, percents=99)
cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.001)

# logger
cerebro.addwriter(
	bt.WriterFile, 
	out=os.path.join(logdir, logfile),
	csv=True)

# run
cerebro.run()

# save report
plt.rcParams['figure.figsize'] = [13.8, 10]
fig = cerebro.plot(style='candlestick', barup='green', bardown='red')
fig[0][0].savefig(
	os.path.join(reportdir, figfile),
	dpi=480)