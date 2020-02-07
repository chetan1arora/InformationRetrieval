#OS libraries
import os,sys
import operator
#NLP library used
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk import regexp_tokenize
from nltk.util import ngrams

#Stemming PorterStemmer
from nltk.stem import PorterStemmer

#lemmatizing WordNetlemmatizer 
from nltk.stem import WordNetLemmatizer


#HTML parsing library
import bs4

def plot(tokenList):
	p = nltk.FreqDist(tokenList)
	pid = os.fork()
	if pid==0:
		p.plot(30,cumulative=False)
		sys.exit()
	return

def findPatterns(listOfWords):
	unigrams = listOfWords
	bigrams = ngrams(listOfWords,2)
	trigrams = ngrams(listOfWords,3)
	plot(listOfWords)
	plot(bigrams)
	plot(trigrams)

# Taking input from file
f = open('../wiki_16','r')
unparsedData = f.read()
f.close()

#Parsing Data using BeautifulSoup

soupData = bs4.BeautifulSoup(unparsedData,features="html.parser")
docList = soupData.select('doc')
data = ' '.join([tag.getText().lower() for tag in docList])

# # Cleaning Data from additional characters like comma,etc.
# escapeWords = ['\n','  ','(',')','.','{','}','-','"','\'','?','#','*','@','$','%','&','[',']','/']
# for w in escapeWords:
# 	while(data.count(w)):
# 		data = data.replace(w,' ' if w in ('\n','  ') else '')

#Using nltk libraries for making ngrams
listOfWords = [x for x in regexp_tokenize(data,r'[?"\s(),.&-]', gaps=True) if x not in ('',' ')]

# #Without stemming and lemmatization
# findPatterns(listOfWords)


# # Stemming process
# stemmer = PorterStemmer()
# stemProcessedWords = [stemmer.stem(w) for w in listOfWords]
# findPatterns(stemProcessedWords)


# # lemmatization process
# lemmatizer = WordNetLemmatizer()
# lemmatizedWords = [lemmatizer.lemmatize(w) for w in listOfWords]
# findPatterns(lemmatizedWords)


#Chi-Square test for finding bi-gram collocations
bigrams = [x for x in ngrams(listOfWords,2)]
# Occurances and Expentances
ocs = {}
firstOcs = {}
lastOcs = {}
chiValues = {}
for bigram in bigrams:
	if bigram in ocs:
		ocs[bigram] += 1
	else:
		ocs[bigram] = 1
		if bigram[0] in firstOcs:
			firstOcs[bigram[0]] += 1
		else:
			firstOcs[bigram[0]] = 1
		if bigram[1] in lastOcs:
			lastOcs[bigram[1]] += 1
		else:
			lastOcs[bigram[1]] = 1

N = len(bigrams)
for bg in ocs:
	O = ocs[bg]
	E = (firstOcs[bg[0]]*lastOcs[bg[1]])/N
	chiSquare = (O-E)*(O-E)/E
	#Checking if chiSquare is comparable to 3.8 (probability distribution for 0.05)
	chiValues[bg] = chiSquare

sorted_values = sorted(chiValues.items(),key=operator.itemgetter(1),reverse=True)

for i in range(20):
	print(sorted_values[i][0],end=',')


