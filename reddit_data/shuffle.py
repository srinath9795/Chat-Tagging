import random
subreddits = ['technology','sports']
data = []
for subreddit in subreddits:
	f = open(subreddit+'_AzureML.tsv','r')
	for text in f:
		text=text.strip()
		text=text.decode('utf-8')
		data.append(text)
f = open('4subReddits.txt','r')
for text in f:
	text=text.strip()
	text=text.decode('utf-8')
	data.append(text)
# data = np.array(data)
random.shuffle(data)
print 'class\ttext'
for line in data:
	print line