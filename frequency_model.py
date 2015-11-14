import re
import copy
import math
import operator
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize

f = open('stopwords.txt','r')
stops = [l.strip() for l in f]
f.close()

file_names = ['sports','technology','movies','music','politics','programming']
norm_files = {

#'technology':641558,
#'sports':570011,
#'movies':486509,
#'music':511676,
#'politics':784324,
#'programming':832118
        
        }


norm_files_sports = {}

sub_cats = {}
sub_cats['sports'] = ['nba','soccer','baseball','cricket','tennis']

top_words_dict = {}

for fn in file_names:
        norm_files[fn] = 0
	f = open('reddit_top_words/'+fn,'r')
	tmp = [(l.split()[0],int(l.split()[1])) for l in f]
        for x in tmp:
            norm_files[fn]+=x[1]
	top_words_dict[fn] = dict(tmp)
	f.close()

for fn in sub_cats['sports']:
        norm_files_sports[fn] = 0
	f = open('reddit_top_words/sports_top_5000_words/'+fn,'r')
	tmp = [(l.split()[0],int(l.split()[1])) for l in f]
        for x in tmp:
            norm_files_sports[fn] += x[1]
	top_words_dict[fn] = dict(tmp)
	f.close()

#print top_words_dict.keys()

total_freq=0

for x in norm_files:
    total_freq+=norm_files[x]


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
	
	for topic in freq_dic:		
		print topic,freq_dic_ind[topic],freq_dic[topic],float(freq_dic[topic])/norm_files[topic]
		freq_dic[topic] = float(freq_dic[topic])/norm_files[topic]
#print freq_dic
	
	if len(freq_dic)==0:
		print  "None"
		return ''
	else:
		tag = max(freq_dic.iteritems(), key=operator.itemgetter(1))[0]
		"""
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
		    """
	cnt = 0
	tmp = ""
	return tag

def getTagNew(msg):
	tag = ""
	# msg = tmp
	removelist = "=& "
	msg = re.sub(r'[^\w'+removelist+']', '',msg).lower()
	lmtzr = WordNetLemmatizer()
    	words = map(lmtzr.lemmatize,msg.split())
	freq_dic = {}
	freq_dic_ind = {}

        score_dic = {}
        for topic in file_names:
            freq_dic[topic] = 0
            score_dic[topic] = 0
            freq_dic_ind[topic] = []

	for word in words:
		if word not in stops:
                        total_word_freq = 0
			for topic in file_names:
				if word in top_words_dict[topic]:
					total_word_freq += top_words_dict[topic][word]
			for topic in file_names:
				if word in top_words_dict[topic]:
                                        pr=float(top_words_dict[topic][word])/norm_files[topic]
                                        pc=float(total_word_freq)/total_freq
                                        score_dic[topic]+=pr*math.log(pr/pc)
					freq_dic[topic] += top_words_dict[topic][word]
					freq_dic_ind[topic] += [(word,top_words_dict[topic][word])]
	
	for topic in freq_dic:		
		print topic,freq_dic_ind[topic],freq_dic[topic],float(freq_dic[topic])/norm_files[topic],score_dic[topic]*10000000
		freq_dic[topic] = float(freq_dic[topic])/norm_files[topic]
#print freq_dic
	
	if len(score_dic)==0:
		print  "None"
		return ''
	else:
		tag = max(score_dic.iteritems(), key=operator.itemgetter(1))[0]
		"""
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
		    """
	cnt = 0
	tmp = ""
	return tag


def getTagNew2(msg):
	tag = ""
	# msg = tmp
	removelist = "=& "
	msg = re.sub(r'[^\w'+removelist+']', '',msg).lower()
	lmtzr = WordNetLemmatizer()
    	words = map(lmtzr.lemmatize,msg.split())
	freq_dic = {}
	freq_dic_ind = {}

        score_dic = {}
        for topic in file_names:
            freq_dic[topic] = 0
            score_dic[topic] = 0
            freq_dic_ind[topic] = []

	for word in words:
		if word not in stops:
                        total_word_freq = 0
			for topic in file_names:
				if word in top_words_dict[topic]:
					total_word_freq += top_words_dict[topic][word]
			for topic in file_names:
				if word in top_words_dict[topic]:
                                        print(word,topic,top_words_dict[topic][word])
                                        pr=float(top_words_dict[topic][word])/norm_files[topic]
                                        pc=float(total_word_freq-top_words_dict[topic][word])/(total_freq-norm_files[topic])
                                        if(pc==0):
                                            pc=0.000000000000001
                                        score_dic[topic]+=pr*math.log(pr/pc)
					freq_dic[topic] += top_words_dict[topic][word]
					freq_dic_ind[topic] += [(word,top_words_dict[topic][word])]
	
	for topic in freq_dic:		
		#print topic,freq_dic_ind[topic],freq_dic[topic],float(freq_dic[topic])/norm_files[topic],score_dic[topic]*10000000
		print topic, score_dic[topic]*10000000
		freq_dic[topic] = float(freq_dic[topic])/norm_files[topic]
#print freq_dic
	
	if len(score_dic)==0:
		print  "None"
		return ''
	else:
		tag = max(score_dic.iteritems(), key=operator.itemgetter(1))[0]
		if tag == "sports":
                        score_dic = {}
			freq_dic = {}
			freq_dic_ind = {}

                        for topic in sub_cats['sports']:
                            score_dic[topic] = 0
                            freq_dic[topic] = 0
                            freq_dic_ind[topic] = []

			for word in words:
				if word not in stops:
					for topic in sub_cats['sports']:
						if word in top_words_dict[topic]:
                                                        pr=float(top_words_dict[topic][word])/norm_files[topic]
                                                        pc=float(total_word_freq-top_words_dict[topic][word])/(total_freq-norm_files[topic])
                                                        if(pc==0):
                                                            pc=0.000000000000001
                                                        score_dic[topic]+=pr*math.log(pr/pc)
                                                        freq_dic[topic] += top_words_dict[topic][word]
                                                        freq_dic_ind[topic] += [(word,top_words_dict[topic][word])]

			sub_tag = max(score_dic.iteritems(), key=operator.itemgetter(1))[0]
			print score_dic
			print tag, sub_tag
	cnt = 0
	tmp = ""
	return tag


def take_input():
    print 'Enter Input'	
    print getTagNew2(raw_input())

def calc_metrics():
    confusionMatrix = {}
    test_data = []
    msg = ""
    file_names = ['sports','technology','movies','music','politics','programming']
    TP={}
    TN={}
    FP={}
    FN={}
    obj = {}
    for fn in file_names:
            obj[fn] = 0	
    for fn in file_names:
            TP[fn] = 0
            TN[fn] = 0
            FP[fn] = 0
            FN[fn] = 0
            confusionMatrix[fn] = copy.deepcopy(obj)
    for fn in file_names:
            f = open('reddit_test_data/'+fn,'r')
            count = 0
            for line in f:
                    count=count+1
                    msg=msg+line
                    if(count==10):
                            test_data.append((msg,fn))
                            count=0
                            
                            pTag = getTagNew2(msg)
                            if pTag!='':
                                confusionMatrix[fn][pTag]+=1
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
    print confusionMatrix

if __name__ == '__main__':
    #print(norm_files)
    #calc_metrics()
    take_input()
    
