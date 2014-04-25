import sys
import re
import json
from thesaurusExpansion import init_thes, test

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
    hand_sentiment = hand_labeled(in_file)
    sentList = init_thes()
    thes_test = test(tweets, sentList)

    count = 1
    precision = 0
    rouge = 0
    for tweet_id in thes_test.keys():
        str_val = ''
        if thes_test[tweet_id] > 1:
            str_val = "positive"
        elif thes_test[tweet_id] < -1:
            str_val = "negative"
        else:
            str_val = "neutral"
        
        hand_val = ''
        if tweet_id in hand_sentiment.keys():
            hand_val = hand_sentiment[tweet_id]
            if hand_val == "irrelevant":
                continue
        else:
            print "rouge tweeet!"
            rouge += 1
            continue
        if hand_val == str_val:
            precision += 1
        print hand_val + " " + str_val
        count += 1

    print "total tweets evaluated: " + str(count)
    print "Precision: " + str(precision)
    print "Rouge tweets: " + str(rouge)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

