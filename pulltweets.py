from tweetlistener import TweetListener
import time, tweepy, sys

## authentication
username   = 'bgardnuh'
api_key    = 'x'
api_secret = 'x'
key        = 'x'
secret     = 'x'
auth       = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(key, secret)
api        = tweepy.API(auth)

def main():
    track = ['#obamacare',]
 
    listen = TweetListener(api, 'obamacare')
    stream = tweepy.Stream(auth, listen)

    print "Streaming started..."

    try: 
        stream.filter(track = track)
    except:
        print "error!"
        stream.disconnect()

if __name__ == '__main__':
    main()