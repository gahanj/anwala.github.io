import tweepy
import json
import sys
import re

#pull in our keyword and #of needed urls
keyword = sys.argv[1]
neededURLCount = sys.argv[2]


#read in our twitter keys
keys = json.load(open("twitterkeys.json"))
#print(keys)
auth = tweepy.OAuthHandler(keys["consumer_api_key"], keys["api_secret_key"])
auth.set_access_token(keys["access_token"], keys["access_token_secret"])
api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, num_tweets):
        super().__init__()
        self.num_tweets = int(num_tweets)
        self.outFile = open("unparsedURLs.txt", 'a')
        self.errFile = open("error_log", 'a')
        self.foundURLs = 0  #used for output to console as a visual aid
        self.parsedURLCount = 0 #used for output to console as a visual aid.
        self.curious = 0
    def on_status(self, status):
        # regex to extract links from tweet
        parsed_tweet = re.findall('https*:\/\/\S+', status.text)

        self.curious += 1
        for url in parsed_tweet:
            self.outFile.write(url + '\n')
            self.num_tweets -= 1
            self.foundURLs += 1

        if self.foundURLs % 20 == 0:
            print("Found Urls: %d   Tweets Processed: %d" % (self.foundURLs, self.curious))



        # False turns the stream off.
        if self.num_tweets < 1:
            return False

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False



myStreamListener = MyStreamListener(neededURLCount)
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener, tweet_mode='extended')
myStream.filter(track=[keyword], is_async=True)












