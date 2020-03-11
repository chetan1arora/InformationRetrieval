# Basic libraries
import os, math
import operator
import pickle

#NLP library used
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+-')
from nltk.corpus import stopwords
# Since the memory for each docID vs word would take much memory, we used unsorted posting list.

# Making the vector space model.
def initializeMem():
	f = open('postingLists','rb')
	global invertedIndex
	invertedIndex = pickle.load(f)
	f.close()
	f = open('docTitles','rb')
	global docSet
	docSet = pickle.load(f)
	f.close()
# Using notation
base = 2
k= 10
# lnc.ltc
# ddd.qqq

def cosineNorm(wt):
	if(len(wt) == 1):
		return wt
	a = 0
	for i in wt:
		a += i*i
	a = 1/math.sqrt(a)
	wt = [a*x for x in wt]
	return wt

def processQuery(query, NumberOfDocs):
	listOfWords = tokenizer.tokenize(query.lower())
	queryDist = nltk.FreqDist(listOfWords)
	popWords = []
	for x in queryDist:
		if x not in invertedIndex:
			popWords.append(x)
	for x in popWords:
		queryDist.pop(x)
	# If query contains only stop words
	if(queryDist == {}):
		return([],[],[])
	axis = [x for x in queryDist]
	queryWt = [1 + math.log(queryDist[x], base) for x in queryDist]
	idfWt = [math.log(float(NumberOfDocs)/len(invertedIndex[x])) for x in axis]
	queryWt = [queryWt[i]*idfWt[i] for i in range(len(axis))]
	queryWt = cosineNorm(queryWt)
	return (axis,queryWt,queryDist)

def fetchDocuments(axis):
	a = {}
	for word in axis:
		for node in invertedIndex[word]:
			a[node[1]] = 1
	return list(a)


def getTermFrequency(word,docId):
	for node in invertedIndex[word]:
		if(node[1] == docId):
			return (1 + math.log(node[0],base))
	return 0

def weightDoc(axis, docId):
	docWt = []
	for idx in range(len(axis)):
		docWt.append(getTermFrequency(axis[idx], docId))
	docWt = cosineNorm(docWt)
	return docWt

def scoreDoc(qWt, dWt):
	score = 0
	for i in range(len(qWt)):
		score += qWt[i]*dWt[i]
	# print(score)
	return score

def jaccardCoefficient(a,b):
	# a and b being Freq Distributions
	intersecCount =0
	for i in a:
		if(i in b):
			intersecCount += 1
	unionCount = len(a.keys())+len(b.keys())-intersecCount

	return intersecCount/unionCount

def sortByKey(a):
	return a[0]

def sortByJaccardCoefficient(topResults, queryDist, docSet):
	tempResults = []
	for res in topResults:
		title = tokenizer.tokenize(docSet[res[0]].lower())
		coeff = jaccardCoefficient(nltk.FreqDist(title), queryDist)
		tempResults.append((coeff,res))

	tempResults.sort(key=sortByKey,reverse=1)

	topResults = [x[1] for x in tempResults]

	return topResults

def searchDocuments(query,limit):
	(axis,queryWt,queryDist) = processQuery(query,len(docSet))
	if(axis == []):
		return axis
	docList = fetchDocuments(axis)
	scores = {}
	for doc in docList:
		docWt = weightDoc(axis, doc)
		scores[doc] = scoreDoc(queryWt, docWt)

	results = sorted(scores.items(),key=operator.itemgetter(1),reverse=1)
	limit = min(len(results), limit)
	topResults = results[:limit]

	topResults = sortByJaccardCoefficient(topResults,queryDist,docSet)
	return topResults

def showResults(results,docSet):
	for i in range(len(results)):
		print("["+str(i)+"] "+docSet[results[i][0]]) # Change here to include scores

initializeMem()
while(1):
	print("Search engine(wiki AA):",end='')
	query = input() # Free text query
	if(query == 'exit'):
		break
	if(query == ""):
		print("Query can not be empty")
	results = searchDocuments(query, k)
	if results:
		showResults(results,docSet)
	else:
		print("No results Found")