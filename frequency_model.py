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
while True:
	cnt+=1
	tmp += raw_input()+" "
	if cnt<5:
		continue
	msg = tmp
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
			
	print freq_dic
	
	if len(freq_dic)==0:
		print "None"
	else:
		tag = max(freq_dic.iteritems(), key=operator.itemgetter(1))[0]
		if tag == "sports":
			freq_dic = {}
			freq_dic_ind = {}
			for word in words:
				if word not in stops:
					for topic in sub_cats['sports']:
						if word in top_words_dict[topic]:
							if topic not in freq_dic:
								freq_dic[topic] = 0
								freq_dic_ind[topic] = []
							
							freq_dic[topic] += top_words_dict[topic][word]
							freq_dic_ind[topic] += [(word,top_words_dict[topic][word])]
			sub_tag = max(freq_dic.iteritems(), key=operator.itemgetter(1))[0]
			print freq_dic,freq_dic_ind
			print tag, sub_tag
		print tag
	cnt = 0
	tmp = ""
	
	

