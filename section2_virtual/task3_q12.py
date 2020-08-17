from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import pandas as pd
import matplotlib as plt
import numpy as np
import CryptoCompare
import pyfolio as pf
import argparse
import random
import csv
import math

# params
datadir = './data' # data path
logdir = './log' # log path
reportdir = './report' # report path
datafile = 'BTC_USDT_1h.csv' # data file
logfile = 'BTC_USDT_1h_SMACross.csv'
figfile = 'BTC_USDT_1h_SMACross.png'
from_datetime = '2020-01-01 00:00:00' # start time 
to_datetime = '2020-04-01 00:00:00' # end time

# get candle data
data_fetcher = new CryptoCompare()
data_fetcher.get_candle('BTC', 'USDT', '1', '2017-04-01', '2020-04-01', 'binance')
os.rename('./BTC_USDT_1h.csv','./data/BTC_USDT_1h.csv')

title = ['','Name','sma_pfast','sma_pslow','Return','MaxDrawDown','TotalTrades#','WinTrades#',
         'LossTrades#','WinRatio','AverageWin$','AverageLoss$','LongestWinStreak','LongestLossStreak',
         'AverageWinLossRatio','RankReturn','RankMaxDrawDown','RankWinRatio','RankAverageWinLossRatio','Score']
b = open('./log/test.csv', 'a', newline='')
#b = open('./log/BTC_USDT_1h_SMACross.csv', 'a', newline='')
a = csv.writer(b)
a.writerow(title)
b.close()

# Create a Stratey
class SMACross(bt.Strategy):
    pslow_temp = []
    pfast_temp = []    
    for i in range(10,26):
        for j in range(i,51):
            pfast_temp.append(i-5)
            pslow_temp.append(j)

    params = (
        ('maperiod', 15),
        ('printlog', False),
        ('pfast', pfast_temp),
        ('pslow', pslow_temp),
        #('printout', True),
    )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add two sma indicator
        self.sma_5_day = bt.ind.SMA(self.datas[0], period=self.params.pfast[self.params.maperiod])
        self.sma_10_day = bt.ind.SMA(self.datas[0], period=self.params.pslow[self.params.maperiod])
        self.crossover = bt.ind.CrossOver(self.sma_5_day, self.sma_10_day)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self): 
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # Not yet ... we MIGHT BUY if ...
            if self.crossover > 0:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
        else:
            if self.crossover < 0:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)
        ta = self.analyzers.ta.get_analysis()
        dd = self.analyzers.dd.get_analysis()
        avg_win = round(ta.won.pnl.total/ta.won.total,4)
        avg_lose = round(ta.lost.pnl.total/ta.lost.total,4)
        win_lose_ratio = abs(round(avg_win/avg_lose,4))
        items = [self.params.maperiod,'SMACross',self.params.pfast[self.params.maperiod],
                 self.params.pslow[self.params.maperiod],
                 np.round(self.broker.getvalue()/self.broker.startingcash-1,4),
                 round(dd.max.drawdown, 4), ta.won.total+ta.lost.total,
                 ta.won.total,ta.lost.total,round(ta.won.total/(ta.won.total+ta.lost.total),4),
                 avg_win,avg_lose,ta.streak.won.longest,ta.streak.lost.longest,win_lose_ratio,
                 'RankReturn','RankMaxDrawDown','RankWinRatio','RankAverageWinLossRatio','Score']
        b = open('./log/test.csv', 'a', newline='')
        #b = open('./log/BTC_USDT_1h_SMACross.csv', 'a', newline='')
        a = csv.writer(b)
        a.writerow(items)
        b.close()

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    strats = cerebro.optstrategy(
        SMACross,
        maperiod=range(536))

    # feed data
    data = pd.read_csv(
            os.path.join(datadir, datafile), index_col='datetime', parse_dates=True)
    data = data.loc[
        (data.index >= pd.to_datetime(from_datetime)) &
        (data.index <= pd.to_datetime(to_datetime))]
    datafeed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(datafeed)

    # Set our desired cash start
    cerebro.broker.setcash(10000.0)

    # Add a FixedSize sizer according to the stake
    #cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=99)

    # Set the commission
    cerebro.broker.setcommission(commission=0.001)

    # analyzer
    #cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="dd")

    # Run over everything
    results = cerebro.run(maxcpus=1)

    """strat = results[0][0]
    pyfoliozer = strat.analyzers.getbyname('pyfolio')

    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    print('-- RETURNS')
    print(returns)
    print('-- POSITIONS')
    print(positions)
    print('-- TRANSACTIONS')
    print(transactions)
    print('-- GROSS LEVERAGE')
    print(gross_lev)"""