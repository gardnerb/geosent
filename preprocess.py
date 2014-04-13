# Take in a file of raw tweet data
# for each tweet
#   determine location
#   clean tweet data
#   insert into map of location to tweet


import sys
import re
import json

def location(user_location):


    return "Michigan"

# Clean SGML tags from a file
def clean(tweet):

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
    tweet = re.sub("\s[-\.,\/:]+\s", " ", tweet)
    tweet = re.sub("(-|\.|,){2,}", " ", tweet)
    # Remove parenthesis
    tweet = re.sub("(\(|\))", "", tweet)
    # Remove commas that are not in a number
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
    # Split word-letter and letter-word combinations (eg 16degrees)
    tweet = re.sub("([a-z]+)(-?)([0-9]+)", "\g<1> \g<3>", tweet)
    tweet = re.sub("([0-9]+)(-?)([a-z]+)", "\g<1> \g<3>", tweet)
    # Split numerical ranges
    tweet = re.sub("(\d+)-(\d+)", "\g<1> \g<2>", tweet)

    for word in tweet.split(" "):
        if word:
            tweet_data.append(word)

    return tweet_data

def main(argv):

    tweet_dict = dict()

    # Open raw tweet file provided on command line
    tweet_file = open(argv, "r")
    tweet_line = tweet_file.readline().replace("\n", "")
    # For each tweet, process and insert into dict
    while tweet_line:
        tweet_obj = json.loads(tweet_line)
        # Find location
        userProvidedLoc = tweet_obj['user']['location']
        if userProvidedLoc:
            print userProvidedLoc
            loc = location(userProvidedLoc)
        # Get and clean text of tweet
        tweet = tweet_obj['text']
        tweet_content = clean(tweet)
        print tweet.encode('utf-8')
        print tweet_content
        # Insert into dict
        if loc in tweet_dict.keys():
            tweet_dict[loc].append(tweet_content)
        else:
            tweet_dict[loc] = list()
            tweet_dict[loc].append(tweet_content)

        tweet_line = tweet_file.readline().replace("\n", "")


    tweet_file.close()


if __name__ == '__main__':
    main(sys.argv[1])

