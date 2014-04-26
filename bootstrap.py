# Take in a file of raw tweet data
# for each tweet
#   determine location
#   clean tweet data
#   insert into map of location to tweet

# Format of dictionary:
#   tweet_dict[state_abr] = list(list(each, word, in tweet))
#   This can be changed if necessary.

import sys
import re
import json
from nltk.corpus import wordnet as wn
from operator import itemgetter

# strong_pos = 4
# strong_neg = -4

def getSentimentList(sentimentList, filename):
    with open(filename) as f:
        for line in f.readlines():
            line = line.rstrip()
            pair = line.split()
            if pair[0] not in sentimentList:
                if float(pair[1]) > 0:
                    sentimentList[pair[0]] = 1
                else:
                    sentimentList[pair[0]] = -1

    return sentimentList


def synonyms(word, sentimentList):
    list = wn.synsets(word)
    score = 0
    for similarWord in list:
        for word in similarWord.lemma_names:
            word = word.lower()
            if word in sentimentList:
                score += sentimentList[word]
    #takes the average of the words
    if score > 0:
        score = 1
    elif score < 0:
        score = -1
    return score

#assuming tweet is a string
def calculateSentiment(tweet, sentimentList):
    tweetWords = tweet.split()
    tweetValue = 0
    pos_count = 0
    neg_count = 0
    for word in tweetWords:
        if "https?" in word:
            continue
        if word not in sentimentList:
            syn = synonyms(word, sentimentList)
            tweetValue += syn
            if syn < 0:
                neg_count += 1
            else: 
                pos_count += 1
        else:
            syn = sentimentList[word]
            #print word, sentimentList[word]
            tweetValue += syn
            if syn < 0:
                neg_count += 1
            else: 
                pos_count += 1

    if pos_count > neg_count:
        return (pos_count + 0.0) / (pos_count + neg_count + 0.0)
    elif neg_count > pos_count:
        return (neg_count + 0.0) / (pos_count + neg_count + 0.0)
    else:
        return 0.0


# Clean SGML tags from a file
def clean(tweet):

    tweet = tweet.encode('utf-8', 'ignore')
    #print str(tweet)

    tweet_data = list()
    # Convert all letters to lower case
    tweet = tweet.lower()
    # Remove usernames
    tweet = re.sub("@\w*", "", tweet)
    # Remove "RT" for retweet
    tweet = re.sub("rt", "", tweet)
    # Remove # before words
    tweet = re.sub("#([a-z0-9])", "\g<1>", tweet)
    # Remove commas
    tweet = re.sub("([a-z]), ", "\g<1> ", tweet)
    # Remove periods at end of words
    tweet = re.sub("([a-z]+)(\.|\?|!|;|:) ", "\g<1> ", tweet)
    # Remove quotation marks
    tweet = re.sub("(\'|\")+(\w*)", "\g<2>", tweet)
    tweet = re.sub("(\w*)(\'|\")+", "\g<1>", tweet)
    # Replace commas between letters with a space (eg hello,there)
    tweet = re.sub("([a-z]+),([a-z]+)", "\g<1> \g<2>", tweet)
    # Expand common contractions
    tweet = re.sub("\'ll", " will", tweet)
    tweet = re.sub("\'ve", " have", tweet)
    tweet = re.sub("\'re", " are", tweet)
    tweet = re.sub("n\'t", " not", tweet)
    tweet = re.sub("\'s", " is", tweet)
    # Shrink all repeated spaces
    tweet = re.sub("\s+", " ", tweet)
    
    stopword_file = open("stopwords.txt", "r")
    stopwords = list()
    for line in stopword_file.readlines():
        line = line.rstrip()
        stopwords.append(line)
    stopword_file.close()

    # Remove stopwords
    tweet_final = ''
    for word in tweet.split(" "):
        if word not in stopwords:
            tweet_final = tweet_final + word + " "

    #print tweet.encode('utf-8')
    return tweet_final


#add words to sentiment list previously not there
def bootstrap(tweet, weight, sentimentList):
    tweetWords = tweet.split();
    for word in tweetWords:
        if 'http' in word:
            continue
        if word not in sentimentList:

            sentimentList[word] = weight
            # print "adding " + word
            try:
                with open("./sentLists/sentimentlist.txt", 'a') as f:
                    word = word.replace(u'\u2019', '')
                    f.write('\n'+word+ '\t\t' + str(weight))
            except:
                ggggg = 1
    return sentimentList


def main(argv):

    for x in range(20,81):
        threshold = float(x/100)
        neg_threshold = 0.0 - threshold
        pos_threshold = 0.0 + threshold

        tweet_list = []
        # tweet_dict = {}
        tweet_score = dict()

        # Open raw tweet file provided on command line
        tweet_file = open(argv, "r")
        tweet_line = tweet_file.readline().replace("\n", "")

        loc = ''
        # For each tweet, process and insert into dict
        while tweet_line:
            tweet_obj = json.loads(tweet_line)
            # Get and clean text of tweet
            tweet = tweet_obj['text']
            tweet_content = clean(tweet)
            tweet_list.append(tweet_content)

            tweet_line = tweet_file.readline().replace("\n", "")


        tweet_file.close()
        sentimentList = {}
        sentimentList = getSentimentList(sentimentList, "./sentListssentcpy.txt")

        for t in tweet_list:
            #print key
            tweet_score = calculateSentiment(tweet, sentimentList)
            if tweet_score > pos_threshold:
                sentimentList = bootstrap(tweet, 1, sentimentList)
            elif tweet_score < neg_threshold:
                bootstrap(tweet, -1, sentimentList)
        sentimentList2 = {}
        try:
            w = open("./sentLists/sentimentList" + str(x) + ".txt", 'r')
            for line in w:
                line = line.rstrip()
                pair = line.split()
                sentimentList2[pair[0]] = pair[1]
            w.close()
        except:
            w = open("./sentLists/sentimentList" + str(x) + ".txt", 'w')
            w.close()
        r = open("./sentList/sentimentList" + str(x) + ".txt", 'a')
        for key in sentimentList:
            #try:
            #    slkjflsd = sentimentList[key]
            #    lskjfldsjfl = sentimentList2[key]
            #except:
            #    print "YOU SUCK"
            if key not in sentimentList2:
                try:
                    r.write(key + " " + str(sentimentList[key]) + "\n")
                except:
                    try:
                        word = key.replace(u'\u2019', '')
                        r.write(word + " " + str(sentimentList[key]) + "\n")
                    except:
                        ljlk = 0
        r.close()

        #print tweet_score[key]
    # print tweet_score


if __name__ == '__main__':
    main(sys.argv[1])
