import sys
import re
import json
from bootstrapMap import init_boot, test

def hand_labeled(in_file):
    result_file = open(in_file, "r")

    hand_sentiment = dict()

    for line in result_file:
        line = line.rstrip()
        line = re.sub("\"[a-z]*\",\"", "", line)
        sentiment = re.sub("\".*$", "", line)
        line = re.sub("^[a-z]*\",\"", "", line)
        tweet_id = re.sub("\"", "", line)
        hand_sentiment[tweet_id] = sentiment

    result_file.close()
    return hand_sentiment

def main(in_file, tweets):
    # Create a dictionary of the hand-labeled tweets
    max_returned = 0
    best = 0
    hand_sentiment = hand_labeled(in_file)
    for i in range (20, 81):
        sentFile = "sentimentList" + str(i) + ".txt"
        sentList = init_boot(sentFile)
        boot_test = test(tweets, sentList)

        count = 1
        precision = 0
        rouge = 0
        for tweet_id in boot_test.keys():
            str_val = ''
            if boot_test[tweet_id] > 1:
                str_val = "positive"
            elif boot_test[tweet_id] < -1:
                str_val = "negative"
            else:
                str_val = "neutral"
            
            hand_val = ''
            if tweet_id in hand_sentiment.keys():
                hand_val = hand_sentiment[tweet_id]
                if hand_val == "irrelevant":
                    continue
            else:
                rouge += 1
                continue
            if hand_val == str_val:
                precision += 1
            count += 1

        print "List " + sentFile
        print "\tPrecision: " + str(precision)
        
        if precision > max_returned:
            max_returned = precision
            best = i
    print "The best threshold was " + str(i)

# Input 1: corpus.csv from hand-labeled tweets
# Input 2: raw tweets from hand-labeled collection
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

