import re
import operator
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize

f = open('stopwords.txt','r')
stops = [l.strip() for l in f]
f.close()

file_names = ['sports','technology','movies','music','politics','programming']
sub_cats = {}
sub_cats['sports'] = ['nba','soccer']

top_words_dict = {}

for fn in file_names:
	f = open('reddit_top_words/'+fn,'r')
	tmp = [(l.split()[0],int(l.split()[1])) for l in f]
	top_words_dict[fn] = dict(tmp)
	f.close()

for fn in sub_cats['sports']:
	f = open('reddit_top_words/'+fn,'r')
	tmp = [(l.split()[0],int(l.split()[1])) for l in f]
	top_words_dict[fn] = dict(tmp)
	f.close()

print len(top_words_dict)

cnt = 0
tmp = ""

def getTag(msg):
	tag = ""
	# msg = tmp
	removelist = "=& "
	msg = re.sub(r'[^\w'+removelist+']', '',msg).lower()
	lmtzr = WordNetLemmatizer()
    	words = map(lmtzr.lemmatize,msg.split())
	freq_dic = {}
	freq_dic_ind = {}
	for word in words:
		if word not in stops:
			for topic in file_names:
				if word in top_words_dict[topic]:
					if topic not in freq_dic:
						freq_dic[topic] = 0
						freq_dic_ind[topic] = []
								
					freq_dic[topic] += top_words_dict[topic][word]
					freq_dic_ind[topic] += [(word,top_words_dict[topic][word])]
			
	# print freq_dic
	
	if len(freq_dic)==0:
		print msg
		print "--------------------------"
		return ""
	else:
		tag = max(freq_dic.iteritems(), key=operator.itemgetter(1))[0]
		# if tag == "sports":
		# 	freq_dic = {}
		# 	freq_dic_ind = {}
		# 	for word in words:
		# 		if word not in stops:
		# 			for topic in sub_cats['sports']:
		# 				if word in top_words_dict[topic]:
		# 					if topic not in freq_dic:
		# 						freq_dic[topic] = 0
		# 						freq_dic_ind[topic] = []
							
		# 					freq_dic[topic] += top_words_dict[topic][word]
		# 					freq_dic_ind[topic] += [(word,top_words_dict[topic][word])]
		# 	sub_tag = max(freq_dic.iteritems(), key=operator.itemgetter(1))[0]
		# 	print freq_dic,freq_dic_ind
		# 	print tag, sub_tag
	cnt = 0
	tmp = ""
	return tag
	
test_data = []
msg = ""
file_names = ['sports','technology','movies','music','politics','programming']
TP={}
TN={}
FP={}
FN={}
for fn in file_names:
	TP[fn] = 0
	TN[fn] = 0
	FP[fn] = 0
	FN[fn] = 0
for fn in file_names:
	f = open('reddit_test_data/'+fn,'r')
	count = 0
	for line in f:
		count=count+1
		msg=msg+line
		if(count==5):
			test_data.append((msg,fn))
			count=0
			
			pTag = getTag(msg)
			if pTag == fn:
				TP[fn]+=1
			elif pTag!='':
				print msg,fn,pTag
				print "==============================	"
				FP[pTag]+=1			
				FN[fn]+=1			
			msg=""
	f.close()
for fn in file_names:
	print '---- for ',fn
	print 'Recall: ',(1.0*TP[fn])/(TP[fn]+FN[fn])
	print 'Precision: ',(1.0*TP[fn])/(TP[fn]+FP[fn])
print TP
print FP
print FN