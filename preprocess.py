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

def sentimentL1(sentimentList, sList):
    s = open(sList, 'r')
    for line in s:
        line = line.rstrip()
        pair = line.split()
        if pair[0] not in sentimentList:
            if pair[1] > 0:
                sentimentList[pair[0]] = 1
            else:
                sentimentList[pair[0]] = -1
    s.close()
    return sentimentList

def sentimentL2(sentimentList, sList, value):
    s = open(sList, 'r')
    i = 1
    for line in s:
        line = line.rstrip()
        if i > 35:
            if line not in sentimentList:
                if value > 0:
                    sentimentList[line] = 1
                else:
                    sentimentList[line] = -1
        i += 1
    s.close()
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
    for word in tweetWords:
        if word not in sentimentList:
            syn = synonyms(word, sentimentList)
            tweetValue += syn
            print word, syn
            if syn < 0:
                print "HURRAY!!!!"
        else:
            syn = sentimentList[word]
            print word, sentimentList[word]
            tweetValue += syn
            if syn < 0:
                print "HURRAY!!!!"
    return tweetValue

def location(user_loc):
    user_loc = user_loc.lower()
    user_loc = re.sub("\n", "", user_loc)
    # Many users say they're from "People's Republic of Chicago". This
    # is just a catch-all for a special case.
    if re.search("chicago", user_loc):
        return "il"
    # Replace commas with spaces
    user_loc = re.sub(",", " ", user_loc)
    # Remove periods
    user_loc = re.sub("\.", "", user_loc)
    # Attempt to find state abbreviation
    state_code = re.search(" ([a-z]{2})(\s+|$)", user_loc)
    if (state_code):
        abv = state_code.group(1)
        if abv == "al": return "al"
        elif abv == "ak": return "ak"
        elif abv == "az": return "az"
        elif abv == "ar": return "ar"
        elif abv == "ca": return "ca"
        elif abv == "co": return "co"
        elif abv == "ct": return "ct"
        elif abv == "de": return "de"
        elif abv == "dc": return "dc"
        elif abv == "fl": return "fl"
        elif abv == "ga": return "ga"
        elif abv == "hi": return "hi"
        elif abv == "id": return "id"
        elif abv == "il": return "il"
        # Could do further checking for the word "in"
        elif abv == "in": return "in"
        elif abv == "ia": return "ia"
        elif abv == "ks": return "ks"
        elif abv == "ky": return "ky"
        elif abv == "la": return "la"
        elif abv == "me": return "me"
        elif abv == "md": return "md"
        elif abv == "ma": return "ma"
        elif abv == "mi": return "mi"
        elif abv == "mn": return "mn"
        elif abv == "ms": return "ms"
        elif abv == "mo": return "mo"
        elif abv == "mt": return "mt"
        elif abv == "ne": return "ne"
        elif abv == "nv": return "nv"
        elif abv == "nh": return "nh"
        elif abv == "nj": return "nj"
        elif abv == "nm": return "nm"
        elif abv == "ny": return "ny"
        elif abv == "nc": return "nc"
        elif abv == "nd": return "nd"
        elif abv == "oh": return "oh"
        elif abv == "ok": return "ok"
        elif abv == "or": return "or"
        elif abv == "pa": return "pa"
        elif abv == "ri": return "ri"
        elif abv == "sc": return "sc"
        elif abv == "sd": return "sd"
        elif abv == "tn": return "tn"
        elif abv == "tx": return "tx"
        elif abv == "ut": return "ut"
        elif abv == "vt": return "vt"
        elif abv == "va": return "va"
        elif abv == "wa": return "wa"
        elif abv == "wv": return "wv"
        elif abv == "wi": return "wi"
        elif abv == "wy": return "wy"

    if re.search("alabama", user_loc): return "al"
    elif re.search("alaska", user_loc): return "ak"
    elif re.search("arizona", user_loc): return "az"
    elif re.search("arkansas", user_loc): return "ar"
    elif re.search("california", user_loc): return "ca"
    elif re.search("colorado", user_loc): return "co"
    elif re.search("connecticut", user_loc): return "ct"
    elif re.search("delaware", user_loc): return "de"
    elif re.search("florida", user_loc): return "fl"
    elif re.search("georgia", user_loc): return "ga"
    elif re.search("hawaii", user_loc): return "hi"
    elif re.search("idaho", user_loc): return "id"
    elif re.search("illinois", user_loc): return "il"
    elif re.search("indiana", user_loc): return "in"
    elif re.search("iowa", user_loc): return "ia"
    elif re.search("kansas", user_loc): return "ks"
    elif re.search("kentucky", user_loc): return "ky"
    elif re.search("louisiana", user_loc): return "la"
    elif re.search("maine", user_loc): return "me"
    elif re.search("maryland", user_loc): return "md"
    elif re.search("massachusetts", user_loc): return "ma"
    elif re.search("michigan", user_loc): return "mi"
    elif re.search("minnesota", user_loc): return "mn"
    elif re.search("mississippi", user_loc): return "ms"
    elif re.search("missouri", user_loc): return "mo"
    elif re.search("montana", user_loc): return "mt"
    elif re.search("nebraska", user_loc): return "ne"
    elif re.search("nevada", user_loc): return "nv"
    elif re.search("new hampshire", user_loc): return "nh"
    elif re.search("new jersey", user_loc): return "nj"
    elif re.search("new mexico", user_loc): return "nm"
    elif re.search("new york", user_loc): return "ny"
    elif re.search("north carolina", user_loc): return "nc"
    elif re.search("north dakota", user_loc): return "nd"
    elif re.search("ohio", user_loc): return "oh"
    elif re.search("oklahoma", user_loc): return "ok"
    elif re.search("oregon", user_loc): return "or"
    elif re.search("pennsylvania", user_loc): return "pa"
    elif re.search("rhode island", user_loc): return "ri"
    elif re.search("south carolina", user_loc): return "sc"
    elif re.search("south dakota", user_loc): return "sd"
    elif re.search("tennessee", user_loc): return "tn"
    elif re.search("texas", user_loc): return "tx"
    elif re.search("utah", user_loc): return "ut"
    elif re.search("vermont", user_loc): return "vt"
    elif re.search("virginia", user_loc): return "va"
    elif re.search("washington", user_loc): return "wa"
    elif re.search("west virginia", user_loc): return "wv"
    elif re.search("wisconsin", user_loc): return "wi"
    elif re.search("wyoming", user_loc): return "wy"
    elif re.search("nyc", user_loc): return "ny"
    elif re.search("new york city", user_loc): return "ny"
    elif re.search("houston", user_loc): return "tx"
    elif re.search("los angeles", user_loc): return "ca"
    elif re.search("seattle", user_loc): return "wa"
    elif re.search("san francisco", user_loc): return "ca"
    elif re.search("phoenix", user_loc): return "az"
    elif re.search("las vegas", user_loc): return "nv"
    elif re.search("miami", user_loc): return "fl"
    else: return "null"    

# Clean SGML tags from a file
def clean(tweet):

    tweet = tweet.encode('utf-8', 'ignore')
    #print str(tweet)

    tweet_data = list()
    # Convert all letters to lower case
    tweet = tweet.lower()
    # Remove URLs
    tweet = re.sub("http[a-z0-9:\/-?\.#+=]* ", "", tweet)
    # Remove usernames
    tweet = re.sub("@\w*", "", tweet)
    # Remove "RT" for retweet
    tweet = re.sub("rt", "", tweet)
    # Remove numbers
    tweet = re.sub("[0-9]*", "", tweet)
    # Remove unnecessary punctuation
    #tweet = re.sub("\s[-\.,\/:]+\s", " ", tweet)
    #tweet = re.sub("(-|\.|,){2,}", " ", tweet)
    # Remove parenthesis
    #tweet = re.sub("(\(|\))", "", tweet)
    # Remove commas
    tweet = re.sub("([a-z]), ", "\g<1> ", tweet)
    # Remove periods at end of words
    tweet = re.sub("([a-z]+)(\.|\?|!|;|:) ", "\g<1> ", tweet)
    # Replace period at end of acronym... kind of hacky
    tweet = re.sub("([a-z\.])\.([a-z]+) ", "\g<1>.\g<2>. ", tweet)
    # Remove periods and commas at end of numbers
    tweet = re.sub("(\d+)(\.|,) ", "\g<1> ", tweet)
    # Remove unnecessary slashes
    tweet = re.sub("( \\\\|\\\\ )", " ", tweet)
    tweet = re.sub("( \/|\/ )", " ", tweet)
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
    
    # Remove stopwords
    #for word in tweet.split(" "):
    #    if word:
    #        tweet_data.append(word)

    #print tweet
    return tweet

def main(argv):

    tweet_dict = dict()
    tweet_score = dict()

    # Open raw tweet file provided on command line
    tweet_file = open(argv, "r")
    tweet_line = tweet_file.readline().replace("\n", "")

    loc = ''
    # For each tweet, process and insert into dict
    while tweet_line:
        tweet_obj = json.loads(tweet_line)
        # Find location
        userProvidedLoc = tweet_obj['user']['location']
        if userProvidedLoc:
            #print userProvidedLoc
            loc = location(userProvidedLoc)
            #print loc
        # Get and clean text of tweet
        tweet = tweet_obj['text']
        tweet_content = clean(tweet)
        #print tweet.encode('utf-8')
        #print tweet_content.encode('utf-8')
        # Insert into dict
        if loc in tweet_dict.keys():
            tweet_dict[loc].append(tweet_content)
        else:
            tweet_dict[loc] = list()
            tweet_score[loc] = 0
            tweet_dict[loc].append(tweet_content)

        tweet_line = tweet_file.readline().replace("\n", "")


    tweet_file.close()
    sentimentList = {}
    print "first round"
    sentimentList = sentimentL1(sentimentList, 'unigrams-pmilexicon1.txt')
    print "second round"
    sentimentList = sentimentL1(sentimentList, 'unigrams-pmilexicon2.txt')
    print "third round"
    sentimentList = sentimentL2(sentimentList, 'positive-words.txt', 1)
    print "fourth round"
    print sentimentList['stuttered']

    sentimentList = sentimentL2(sentimentList, 'negative-words.txt', -1)

    print sentimentList['stuttered']
    for key in tweet_dict.keys():
        #print key
        for tweet in tweet_dict[key]:
            tweet_score[key] += calculateSentiment(tweet, sentimentList)
        #print tweet_score[key]
    print tweet_score


if __name__ == '__main__':
    main(sys.argv[1])

