#!/usr/bin/env python
# coding: utf-8
import os
import collections

import numpy as np

from SMACross import *
from utils import OptStrategy

if __name__ == "__main__":
    cerebro.addanalyzer(bt.analyzers.Returns, _name='ret')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="dd")
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')

    cerebro.optstrategy(SMACross,
                        sma_pfast=range(5, 21, 1), sma_pslow=range(10, 51, 1))
    thestrats = cerebro.run()

    outfile = '_'.join([
        os.path.splitext(datafile)[0],
        thestrats[0][0].strategycls.__name__]) + '.csv'
    outfilepath = os.path.join(reportdir, outfile)
    OptStrategy(thestrats).get_rank(outfilepath)
