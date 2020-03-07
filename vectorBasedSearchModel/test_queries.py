# Basic libraries
import os, math
import operator
import pickle

#NLP library used
import nltk
# nltk.download('punkt')
from nltk import regexp_tokenize

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
	a = 0
	for i in wt:
		a += i*i

	a = 1/math.sqrt(a)
	wt = [a*x for x in wt]
	return wt

def processQuery(query, NumberOfDocs):
	listOfWords = [x for x in regexp_tokenize(query.lower(),r'[?"\'\s(),.&\-]', gaps=True) if x not in ('',' ')]
	queryDist = nltk.FreqDist(listOfWords)
	axis = [x for x in queryDist]
	queryWt = [1 + math.log(queryDist[x], base) for x in queryDist]
	# Term not being in the invertedIndex (Take case)
	idfWt = [math.log(float(NumberOfDocs)/len(invertedIndex[x])) for x in axis]
	queryWt = [queryWt[i]*idfWt[i] for i in range(len(axis))]
	queryWt = cosineNorm(queryWt)
	return (axis,queryWt)

def fetchDocuments(axis):
	a = {}
	for word in axis:
		for node in invertedIndex[word]:
			a[node[1]] = 1
	return list(a)


def getTermFrequency(word,docId):
	for node in invertedIndex[word]:
		if(node[1] == docId):
			return node[0]
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

def searchDocuments(query):
	(axis,queryWt) = processQuery(query,len(docSet))
	# for i in range(len(axis)):
	# 	print(axis[i]+":"+str(queryWt[i]))
	# 	for j in invertedIndex[axis[i]]:
	# 		print(j)

	docList = fetchDocuments(axis)
	scores = {}
	for doc in docList:
		docWt = weightDoc(axis, doc)
		scores[doc] = scoreDoc(queryWt, docWt)

	topResults = sorted(scores.items(),key=operator.itemgetter(1),reverse=1)
	return topResults

def showResults(results,limit,docSet):
	limit = min(len(results), limit)
	for i in range(limit):
		print("["+str(i)+"] "+docSet[results[i][0]])

initializeMem()
while(1):
	print("Search engine(wiki AA):",end='')
	query = input() # Free text query
	if(query == 'exit'):
		break
	if(query == ""):
		print("Query can not be empty")
	results = searchDocuments(query)
	showResults(results,k,docSet)

