#!/usr/bin/env python

import tweepy
import json

cred = open('credentials.txt')

## authentication
username   = 'bgardnuh'
api_key    = cred.readline().strip()
api_secret = cred.readline().strip()
key        = cred.readline().strip()
secret     = cred.readline().strip()
auth       = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(key, secret)
api        = tweepy.API(auth)


id_file = open("tweet_id_list.txt", "r")
json_out = open("evalTweets.json", "w")

num_fails = 0
num_tweets = 1
for line in id_file:
    print "Fetching tweet " + str(num_tweets)
    num_tweets += 1
    line.rstrip()
    results = ''
    try:
        results = api.get_status(line)
    except:
        num_fails += 1
        print "failure " + str(num_fails)
        pass
    #print results._json
    if results != '':
        json_out.write(str(results._json) + "\n")


id_file.close()
json_out.close()
