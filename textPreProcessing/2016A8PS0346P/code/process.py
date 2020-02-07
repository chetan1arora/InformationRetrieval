import bs4

# Taking input from file
f = open('../wiki_16','r')
unparsedData = f.read()
f.close()
#Parsing Data using BeautifulSoup
soupData = bs4.BeautifulSoup(unparsedData)
print(type(soupData))
docList = soupData.select('doc')
data = ' '.join([tag.getText() for tag in docList])

# Cleaning Data from additional characters like comma,etc.
escapeWords = ['\n','  ','(',')','.','{','}','-','"','\'','?','#','*','@','$','%','&','[',']','/']
for w in escapeWords:
	while(data.count(w)):
		data = data.replace(w,' ' if w in ('\n','  ') else '')

# Now Making a list of all the words in the data
splitData = data.split(' ')
listOfWords = [x.strip() for x in data.split(' ')]

for i in range(100):
	print(splitData[i])
	print(listOfWords[i],end =',')
# g = open('cleanData.txt','w')
# g.write(listOfWords)
# g.close()