from nltk import word_tokenize, pos_tag, chunk, RegexpParser, pos_tag, FreqDist, tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import json
import csv
import re

from operator import itemgetter

#Untuk StopWord
csv.field_size_limit(500000)
infile=open('StopWordEnglish.dic')
infile2=open('NotImportantWords.dic')
infile3=open('positive-words.txt')
infile4=open('negative-words.txt')

stop_words = list()
not_important_word = list()

list_positive_words = list()
list_negative_words = list()


#Adding stop word data
for line in infile:
    stop_words.append(line[:-1:])

for line in infile2:
    not_important_word.append(line[:-1:])

for line in infile3:
    list_positive_words.append(line[:-1:])

for line in infile4:
    list_negative_words.append(line[:-1:])

#fungsi untuk load dataset
def load_data(dataset):
    sentences = []
    labels = []
    
    with open(dataset, 'rU') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
               text = row['text']
               type = row['type']

               sentences.append(text)
               labels.append(type)
            except:
                continue
    return sentences, labels

def removeStopWord(arraySentence):
	arraySentenceOut = list()
	for sentence in arraySentence:
		try:
		#list temporary untuk menampung kata-kata bebas stopword dalam suatu kalimat
			tempArr = list();

			for tempWord in word_tokenize(sentence):

				#print (tempWord)
				if (tempWord not in stop_words) and ('https' not in tempWord) and ('//https' not in tempWord) and ('//' not in tempWord) and ('//t.co/' not in tempWord) and ('@' not in tempWord):
					tempArr.append(tempWord)

					#Debug apakah kata ter filter dalam stopwords
					#print (tempWord, 'lolos')

			temp_sentence = ""
			for word in tempArr:
				temp_sentence = temp_sentence + word + " "

			temp_sentence = temp_sentence[:-1:]
			arraySentenceOut.append(temp_sentence)
		except:
			continue

	return arraySentenceOut

def removeNotImportantWord(arraySentence):
	arraySentenceOut = list()
	regexp = re.compile(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)')

	for sentence in arraySentence:
		try:
		#list temporary untuk menampung kata-kata bebas stopword dalam suatu kalimat
			tempArr = list();

			for tempWord in word_tokenize(sentence):
				
				#print (tempWord)
				if tempWord not in not_important_word and ('https' not in tempWord) and ('//https' not in tempWord) and ('//' not in tempWord) and ('//t.co/' not in tempWord) and (not (regexp.search(tempWord))):
					tempArr.append(tempWord)

					#Debug apakah kata ter filter dalam stopwords
					#print (tempWord, 'lolos')

			temp_sentence = ""
			for word in tempArr:
				temp_sentence = temp_sentence + word + " "

			temp_sentence = temp_sentence[:-1:]
			arraySentenceOut.append(temp_sentence)
		except:
			continue

	return arraySentenceOut


def toLowerCase(arraySentence):
	arraySentenceOut = list()
	for sentence in arraySentence:
		arraySentenceOut.append(str.lower(sentence))

	return arraySentenceOut

def toLemmatization(arraySentence):
	wordnet_lemmatizer = WordNetLemmatizer()
	arraySentenceOut = list()
	for sentence in arraySentence:
		try:
			#list temporary untuk menampung kalimat dengan bentuk lemma
			tempArr = list();

			for tempWord in word_tokenize(sentence):
				tempArr.append(wordnet_lemmatizer.lemmatize(tempWord))

			temp_sentence = ""
			for word in tempArr:
				temp_sentence = temp_sentence + word + " "

			temp_sentence = temp_sentence[:-1:]
			arraySentenceOut.append(temp_sentence)
		except:
			continue

	return arraySentenceOut

def extractAdj(arraySentence):
	arraySentenceOut = list()

	for tweet in arraySentence:
		tagged = pos_tag(word_tokenize(tweet))

		tempWord = [a for (a,_) in tagged]
		tempTag = [b for (_,b) in tagged]

		for i in range(len(tempWord)):
			if((tempWord[i]!='trump' and tempWord[i]!='russian') and (tempTag[i]=='JJ' or tempTag[i]=='JJR' or tempTag[i]=='JJS')):
				arraySentenceOut.append(tempWord[i])

		return arraySentenceOut;

def displayNounPhrase(tweet):
	sentence = word_tokenize(tweet)
	tagged_sentence = pos_tag(sentence)

	tree_result = cp.parse(tagged_sentence)

	#extract only NP
	for subtree in tree_result.subtrees():
	    if subtree.label() == 'NP': 
	        subtree.leaves()

fileOpen = open('trump.tweets', 'r' ,encoding="utf8")

listTweets = list()

for line in fileOpen:
	try:
		listTweets.append(line)
	except:
		continue

# listTweets = removeStopWord(listTweets)

listTweets = removeNotImportantWord(listTweets)
print(listTweets)

# listTweets = toLowerCase(listTweets)

# listTweets = toLemmatization(listTweets)

adjList = extractAdj(listTweets)

count_positive = 0;
count_negative = 0;
count_uncategorized = 0;

uncategorizedAdjList = dict()
positiveAdjList = dict()
negativeAdjList = dict()

for word in adjList:
	if word in list_positive_words:
		count_positive = count_positive + 1;
		if word in positiveAdjList:
			positiveAdjList[word] = positiveAdjList[word] + 1
		else:
			positiveAdjList[word] = 1
	elif word in list_negative_words:
		count_negative = count_negative + 1;
		if word in negativeAdjList:
			negativeAdjList[word] = negativeAdjList[word] + 1
		else:
			negativeAdjList[word] = 1
	else:
		count_uncategorized = count_uncategorized + 1;
		if word in uncategorizedAdjList:
			uncategorizedAdjList[word] = uncategorizedAdjList[word] + 1
		else:
			uncategorizedAdjList[word] = 1


grammar = r"""
  NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
      {<NNP>+}                # chunk sequences of proper nouns
"""

cp = RegexpParser(grammar)

for tweet in listTweets:
	displayNounPhrase(tweet)