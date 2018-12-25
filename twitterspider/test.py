import tweepy
import re

consumer_key = 'hfJdo98qyoA8DXMCjebi1MSz8'
consumer_secret = 'j5KTTKWSaHBzHV6Tub7Aa5yMc2RGdn8bwYrcmNjYSiSx8P3vUn'

access_token = '320039612-PYcQK81jsIqx6OUH6nZAzi5ovSbpLeVaBfGd4cuB'
access_token_secret = 'T9nEIFmTbCpqPr2ndwpbcJNSwtNz2BpZcdI7WmBkLpMRC'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
target = open("tweets.txt", 'w',encoding="utf-8")
# for tweet in tweepy.Cursor(api.user_timeline,id='USATODAY').items():
#     print(tweet.text)

tweets = api.search('長時間労働',count = 20000)

for t in tweets:
    line = re.sub("[A-Za-z:/#\. @︎…]","",t.text)
    print(line)
    target.write(line + '\n')



target.close()
