#modified from http://badhessian.org/2012/10/collecting-real-time-twitter-data-with-the-streaming-api/

from tweepy import StreamListener
import json, time, sys

class TweetListener(StreamListener):


    def __init__(self, api = None, fprefix = 'streamer'):
        self.api = api or API()
        self.counter = 0
        self.fprefix = fprefix
        self.output  = open(fprefix + '.' 
                            + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
        self.delout  = open('delete.txt', 'a')


    def on_data(self, data):
        
        jsondata = json.loads(data)
        if jsondata["coordinates"] != None:
            print "here!"
            self.on_status(data)
            #not sure what these parts do
            # if 'limit' in data:
            #     if self.on_limit(json.loads(data)['limit']['track']) is False:
            #         return False
            # elif 'warning' in data:
            #     warning = json.loads(data)['warnings']
            #     print warning['message']
            #     return False
        elif jsondata["user"]["location"] != None:
            print "user loc"
            self.on_status(data)


    def on_status(self, status):
        self.output.write(status + "\n")

        self.counter += 1

        if self.counter >= 20000:
            self.output.close()
            self.output = open('../streaming_data/' + self.fprefix + '.' 
                            + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
            self.counter = 0

        return True


    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return True


    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False


    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return True

