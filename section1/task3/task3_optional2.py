"""
Copyright (c) 2018 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from crypto_news_api import CryptoControlAPI
import pandas as pd

# Connect to the CryptoControl API
api = CryptoControlAPI(open("task3_api.txt", "r").read())

# Get top news
top_news = api.getTopNews()
df = pd.DataFrame(top_news)
df = df.drop(['similarArticles', 'coins', 'source','description','originalImageUrl','url','thumbnail'], axis=1)
df.to_csv('top_news_data.csv',index=False)

# get latest russian news
ru = api.getLatestNews("ru")
df = pd.DataFrame(ru)
df = df.drop(['similarArticles', 'coins', 'source','description','originalImageUrl','url','thumbnail'], axis=1)
df['title'].apply(lambda x: x.strip())
df.to_csv('ru_data.csv',index=False)

# get top bitcoin news
bitcoin = api.getTopNewsByCoin("bitcoin")
df = pd.DataFrame(bitcoin)
df = df.drop(['similarArticles', 'coins', 'source','description','originalImageUrl','url','thumbnail'], axis=1)
df.to_csv('bitcoin_data.csv',index=False)

# get top EOS tweets
eos = api.getTopTweetsByCoin("eos")
df = pd.DataFrame(eos)
df = df.drop(['text','url'], axis=1)
df.to_csv('eos_data.csv',index=False)

# get top Ripple reddit posts
ripple = api.getLatestRedditPostsByCoin("ripple")
df = pd.DataFrame(ripple)
df = df.drop(['similarArticles', 'coins', 'source','description','originalImageUrl','url','thumbnail'], axis=1)
df.to_csv('ripple_data.csv',index=False)

# get reddit/tweets/articles in a single combined feed for NEO
neo = api.getTopFeedByCoin("neo")
df = pd.DataFrame(neo)
df1 = pd.DataFrame(df[df['type']=='article'].article.tolist())
df2 = pd.DataFrame(df[df['type']=='reddit'].reddit.tolist())
df3 = pd.DataFrame(df[df['type']=='tweet'].tweet.tolist())
df1 = df1.drop(['similarArticles', 'coins', 'source','description','originalImageUrl','url','thumbnail'], axis=1)
df2 = df2.drop(['description','url'], axis=1)
df3 = df3.drop(['text','url'], axis=1)
df1.to_csv('neo_article_data.csv',index=False)
df2.to_csv('neo_reddit_data.csv',index=False)
df3.to_csv('neo_tweet_data.csv',index=False)

# get latest reddit/tweets/articles (seperated) for Litecoin
litecoin = api.getLatestItemsByCoin("litecoin")
df = pd.DataFrame(litecoin)
df1 = pd.DataFrame(df[df['type']=='article'].article.tolist())
df2 = pd.DataFrame(df[df['type']=='reddit'].reddit.tolist())
df3 = pd.DataFrame(df[df['type']=='tweet'].tweet.tolist())
df1 = df1.drop(['similarArticles', 'coins', 'source','description','originalImageUrl','url','thumbnail'], axis=1)
df2 = df2.drop(['description','url'], axis=1)
df3 = df3.drop(['text','url'], axis=1)
df1.to_csv('litecoin_article_data.csv',index=False)
df2.to_csv('litecoin_reddit_data.csv',index=False)
df3.to_csv('litecoin_tweet_data.csv',index=False)

# get details (subreddits, twitter handles, description, links) for ethereum
ethereum = api.getCoinDetails("ethereum")
df = pd.DataFrame([ethereum])
df.to_csv('ethereum_data.csv',index=False)