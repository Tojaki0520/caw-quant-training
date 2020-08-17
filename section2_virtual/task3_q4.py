import pandas as pd

df = pd.read_csv('./log/test.csv')  

re = list(df['Return'].values)
re.sort(reverse=True)
rank_return = []
for r in list(df['Return'].values):
    rank = re.index(r)
    rank_return.append(rank+1)

mdd = list(df['MaxDrawDown'].values)
mdd.sort(reverse=False)
rank_mdd = []
for r in list(df['MaxDrawDown'].values):
    rank = mdd.index(r)
    rank_mdd.append(rank+1)

w = list(df['WinRatio'].values)
w.sort(reverse=True)
rank_w = []
for r in list(df['WinRatio'].values):
    rank = w.index(r)
    rank_w.append(rank+1)

wl = list(df['AverageWinLossRatio'].values)
wl.sort(reverse=True)
rank_wl = []
for r in list(df['AverageWinLossRatio'].values):
    rank = wl.index(r)
    rank_wl.append(rank+1)

score = [round((a+b+c+d)/4,4) for a,b,c,d in zip(rank_mdd,rank_mdd,rank_w,rank_wl)]
df['RankReturn'] = rank_return
df['RankMaxDrawDown'] = rank_mdd
df['RankWinRatio'] = rank_w
df['RankAverageWinLossRatio'] = rank_wl
df['Score'] = score

df.to_csv('./log/BTC_USDT_1h_SMACross.csv',index=False)