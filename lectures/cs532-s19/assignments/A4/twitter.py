import tweepy
import json
import sys
import re
import time
from bs4 import BeautifulSoup
import urllib.request

#read in our twitter keys
keys = json.load(open("../twitterkeys.json"))
#print(keys)
auth = tweepy.OAuthHandler(keys["consumer_api_key"], keys["api_secret_key"])
auth.set_access_token(keys["access_token"], keys["access_token_secret"])
api = tweepy.API(auth, wait_on_rate_limit=True)

data = []

outFile = open("data.txt", 'a')


try:
    for follower in tweepy.Cursor(api.followers, screen_name="acnwala").items():
        data.append(follower.screen_name)
        print(follower.screen_name)
        outFile.write("%s\n" % follower.screen_name)
except Exception as e:
    print(str(e))


#"https://twitter.com/%s" % entry.strip()
with open('data.txt', 'r') as inFile:
    for entry in inFile:
        with urllib.request.urlopen("https://twitter.com/%s" % entry.strip()) as res:
            baseHMTL = res.read()
            soup = BeautifulSoup(baseHMTL, features="html.parser")

            tags = soup.findAll("span", class_="ProfileNav-value")
            followers = tags[2]
            try:
                followers = followers["data-count"]
                with open('follow_data', 'a') as finalFile:
                    print("%s, %d" % (entry.strip(), int(followers)))
                    finalFile.write("%s, %d\n" % (entry.strip(), int(followers)))
            except KeyError:
                with open('follow_data', 'a') as finalFile:
                    finalFile.write("%s, %d\n" % (entry.strip(), 0))
