from crypto_news_api import CryptoControlAPI
import pandas as pd

# Connect to the CryptoControl API
api = CryptoControlAPI("598fde0838a37ff5834d13107b5eb59e")

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