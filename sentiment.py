import sys
import re
import heapq
import collections
from nltk.corpus import wordnet as wn
from operator import itemgetter

#to install nltk
#type this in the command line: sudo pip install -U pyyaml nltk
#if you don't have pip also run: sudo easy_install pip
#then to get the data files: python -m nltk.downloader all

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
	for line in s:
		line = line.rstrip()
		if line not in sentimentList:
			if value > 0:
				sentimentList[line] = 1
			else:
				sentimentList[line] = -1

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
	else:
		score = -1
	return score

'''
def main(argv):
	sentimentList = {}
	sList1 = 'unigrams-pmilexicon1.txt'
	sList2 = 'unigrams-pmilexicon2.txt'
	sentimentList = sentiment(sentimentList, sList1)
	sentimentList = sentiment(sentimentList, sList2)

	#below is an example of synsets
	#list = wn.synsets("sweet")
	#for word in list:
	#	print word, word.lemma_names
	#looking up "sweets" will produce the following output
	"""
	Synset('sweet.n.01') ['Sweet', 'Henry_Sweet']
	Synset('dessert.n.01') ['dessert', 'sweet', 'afters']
	Synset('sweet.n.03') ['sweet', 'confection']
	Synset('sweet.n.04') ['sweet', 'sweetness', 'sugariness']
	Synset('sweetness.n.02') ['sweetness', 'sweet']
	Synset('sweet.a.01') ['sweet']
	Synset('angelic.s.03') ['angelic', 'angelical', 'cherubic', 'seraphic', 'sweet']
	Synset('dulcet.s.02') ['dulcet', 'honeyed', 'mellifluous', 'mellisonant', 'sweet']
	Synset('sweet.s.04') ['sweet']
	Synset('gratifying.s.01') ['gratifying', 'sweet']
	Synset('odoriferous.s.03') ['odoriferous', 'odorous', 'perfumed', 'scented', 'sweet', 'sweet-scented', 'sweet-smelling']
	Synset('sweet.a.07') ['sweet']
	Synset('fresh.a.06') ['fresh', 'sweet']
	Synset('fresh.s.09') ['fresh', 'sweet', 'unfermented']
	Synset('sugared.s.01') ['sugared', 'sweetened', 'sweet', 'sweet-flavored']
	Synset('sweetly.r.01') ['sweetly', 'sweet']
	"""


if __name__ == "__main__":
	main(sys.argv[1:])
'''