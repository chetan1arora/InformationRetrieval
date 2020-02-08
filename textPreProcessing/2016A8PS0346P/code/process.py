#OS libraries
import os,sys
import operator
#NLP library used
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk import regexp_tokenize
from nltk.util import ngrams
from nltk import pos_tag
from nltk.corpus import wordnet

#Stemming PorterStemmer
from nltk.stem import PorterStemmer

#lemmatizing WordNetLemmatizer 
from nltk.stem import WordNetLemmatizer


#HTML parsing library
import bs4

def plot(tokenList,title):
	p.plot(30,cumulative=False,title=title)
	return

def mostOccuring(dist,p):
	myDict = dist.most_common(len(dist))
	count = 0
	val = 0
	for i,j in myDict:
		val += j
		count += 1
		if(val >= p):
			break
	return str(count)

def findPatterns(listOfWords,title):
	unigrams = listOfWords
	bigrams = list(ngrams(listOfWords,2))
	trigrams = list(ngrams(listOfWords,3))
	pid = os.fork()
	if pid==0:
		#Unigrams
		dist = nltk.FreqDist(listOfWords)
		print("Number of unique unigrams after "+title+" :"+str(len(dist.keys())))
		print("[*]Number of "+title+" unigrams that make up 90%:"+mostOccuring(dist,0.9*len(listOfWords)))
		print("[-]Exit unigrams plot to get bigram plots")
		dist.plot(30,cumulative=False,title=title+' Unigrams')

		#Bigrams
		print("[-]Exit Bigrams plot to get trigram plots")
		dist = nltk.FreqDist(bigrams)
		print("Number of unique bigrams after "+title+" :"+str(len(dist.keys())))
		print("[*]Number of "+title+" bigrams that make up 80%:"+mostOccuring(dist,0.8*len(bigrams)))
		dist.plot(30,cumulative=False,title=title+' Bigrams')		

		#Trigrams
		dist = nltk.FreqDist(trigrams)
		print("Number of unique trigrams after "+title+" :"+str(len(dist.keys())))
		print("[*]Number of "+title+" trigrams that make up 70%:"+mostOccuring(dist,0.7*len(trigrams)))
		dist.plot(30,cumulative=False,title=title+' Trigrams')				
		sys.exit()
	return
def tagWordNet(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
# Taking input from file
# print("Usage:")
	# print("python3 process.py relativePath")
	# sys.exit()
if len(sys.argv)==2:
	f = open(sys.argv[1],'r')
	unparsedData = f.read()
	f.close()
else:
	f=open('wiki_44','r')
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
listOfWords = [x for x in regexp_tokenize(data,r'[?"\s(),.&\-]', gaps=True) if x not in ('',' ')]

#Without stemming and lemmatization
findPatterns(listOfWords,'Tokenized')

# Stemming process
stemmer = PorterStemmer()
stemProcessedWords = [stemmer.stem(w) for w in listOfWords]
findPatterns(stemProcessedWords,'Stemmed')

# lemmatization process
# Pos tagging
taggedWords = pos_tag(listOfWords)
wordNetTaggedWords = [tagWordNet(x[1]) for x in taggedWords]

lemmatizer = WordNetLemmatizer()
lemmatizedWords = [lemmatizer.lemmatize(listOfWords[x],wordNetTaggedWords[x]) for x in range(len(taggedWords))]
findPatterns(lemmatizedWords,'Lemmatized')

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
			lastOcs[bigram[1]] +=1	
		else:
			lastOcs[bigram[1]] = 1

N = len(bigrams)
for bg in ocs:
	O = ocs[bg]
	E = (firstOcs[bg[0]]*lastOcs[bg[1]])/N
	chiSquare = (O-E)*(O-E)/E
	chiValues[bg] = chiSquare

sorted_values = sorted(chiValues.items(),key=operator.itemgetter(1),reverse=True)

print("Collocations found in the text:")
for i in range(20):
	print(sorted_values[i][0])
