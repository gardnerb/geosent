"""
    Reads authentication credentials from 'credentials.txt', which is formated as:

        API key
        API sercret
        Access token
        Access token secret

    Pull tweets get tweets from the twitter Stream API,
    using track as the keyword search
"""

from tweetlistener import TweetListener
import time, tweepy, sys


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

def main():
    track = ['#obamacare',] #change to w/e
    file_prefix = 'obamacare' #change to what you want the file prefixed with 
 
    listen = TweetListener(api, file_prefix)
    stream = tweepy.Stream(auth, listen)

    print "Streaming started..."

    try: 
        stream.filter(track = track)
    except:
        print "error!", sys.exc_info()[0]
        stream.disconnect()

if __name__ == '__main__':
    main()