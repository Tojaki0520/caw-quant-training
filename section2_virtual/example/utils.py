import collections

import backtrader as bt
import numpy as np
import pandas as pd


class OptStrategy():

    def __init__(self, thestrats):
        self.thestrats = thestrats

    def get_result(self, outfile: str = None):
        optresults = []
        for thestart in self.thestrats:
            if thestart == []:
                continue
            optresult = collections.OrderedDict()
            result = thestart[0]
            optresult.update({"Name": result.strategycls.__name__})
            params_dict = result.p.__dict__
            optresult.update(params_dict)
            if result.strategycls.__name__ in ['OBVCross', 'OBVCrossSL']:
                pslow_minus_pfast = params_dict['obv_pslow'] - \
                    params_dict['obv_pfast']
                optresult.update({"PslowMinusPfast": pslow_minus_pfast})
            for analyzer in result.analyzers._items:
                if analyzer.__class__ == bt.analyzers.returns.Returns:
                    ret = np.exp(analyzer.rets['rtot']) - 1
                    msg = {"Return": ret}
                elif analyzer.__class__ == bt.analyzers.drawdown.DrawDown:
                    msg = {"MaxDrawDown": analyzer.rets.max.drawdown}
                elif analyzer.__class__ == bt.analyzers.tradeanalyzer.TradeAnalyzer:
                    if analyzer.rets.total.total != 0:
                        try:
                            ttl_trd = analyzer.rets.total.closed
                        except KeyError:
                            msg = {}
                        else:
                            win_num = analyzer.rets.won.total
                            loss_num = analyzer.rets.lost.total
                            win_ratio = win_num / (win_num + loss_num)
                            win_avg = analyzer.rets.won.pnl.average
                            loss_avg = analyzer.rets.lost.pnl.average
                            lngst_win_strk = analyzer.rets.streak.won.longest
                            lngst_loss_strk = analyzer.rets.streak.lost.longest
                            msg = {
                                "TotalTrades#": ttl_trd, "WinTrades#": win_num, "LossTrades#": loss_num,
                                "WinRatio": win_ratio, "AverageWin$": win_avg, "AverageLoss$": loss_avg,
                                "LongestWinStreak": lngst_win_strk, "LongestLossStreak": lngst_loss_strk}
                optresult.update(msg)
            optresults.append(optresult)
        df = pd.DataFrame(optresults)
        if outfile is not None:
            df.to_csv(outfile, float_format='%.4f')
            print(f"See {outfile} for optimization result")
        return df

    def get_rank(self, outfile: str = None):
        df = self.get_result()
        df['AverageWinLossRatio'] = df['AverageWin$'] / \
            np.abs(df['AverageLoss$'])
        df['RankReturn'] = df['Return'].rank(
            method='min', na_option='bottom', ascending=False).astype('int')
        df['RankMaxDrawDown'] = df['MaxDrawDown'].rank(
            method='min', na_option='bottom', ascending=True).astype('int')
        df['RankWinRatio'] = df['WinRatio'].rank(
            method='min', na_option='bottom', ascending=False).astype('int')
        df['RankAverageWinLossRatio'] = df['AverageWinLossRatio'].rank(
            method='min', na_option='bottom', ascending=False).astype('int')
        df['Score'] = (df['RankReturn'] + df['RankMaxDrawDown'] +
                       df['RankWinRatio'] + df['RankAverageWinLossRatio']) / 4
        if outfile is not None:
            df.to_csv(outfile, float_format='%.4f')
            print(f"See {outfile} for optimization result")
        return df
