import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
from nltk.stem.wordnet import WordNetLemmatizer
import numpy as np
from sklearn import svm
import lda
#import lda.datasets
import re
from collections import defaultdict
from nltk.corpus import stopwords
import operator
# import json
import pprint
pp = pprint.PrettyPrinter()
# with open('item.json') as data_file:    
#     data = json.load(data_file)
#     data = [x['message'] for x in data]
# # pprint(data)
# data = np.array(data)
# print len(data)
# B = np.reshape(data[:-3], (-1, 5))
# print B
import json
import pprint
pp = pprint.PrettyPrinter()


"""Below code reads the file, combines 5 messages into into sentence and returns the list of such sentences in list named 'docs' """

file_names = ['sports.txt','technology.txt']
cnt = 0
docsObj = {}
docs = []
tmp = ""

for fn in file_names:
    jf = open('reddit_data/'+fn,'r')
    docsObj[fn] = []
    for i in jf:
        tmp += i+" "
        cnt+=1
        if cnt==5:
            docsObj[fn] += [(tmp,fn)]
            tmp = ""
            cnt = 0
""" File reading done """
print len(docs)
docs1 = docsObj['sports.txt']
docs2 = docsObj['technology.txt']
docs1 = np.array(docs1)
docs2 = np.array(docs2)
np.random.shuffle(docs1)
np.random.shuffle(docs2)
docs = np.concatenate((docs1[:3000,:] , docs2[:3000,:]))
np.random.shuffle(docs)

""" Remove stop words and build vocabulary """
removelist = "=& "  # for non-alpha numeric chars that are allowed
msgCount = 0
doc_freq_dic = []
vocab = defaultdict(int)
stop = stopwords.words('english')
for msgSet in docs:
    msgSet = msgSet[0]
    msgSet= re.sub(r'[^\w'+removelist+']', '',msgSet).lower()
    lmtzr = WordNetLemmatizer()
    words = map(lmtzr.lemmatize,msgSet.split())
    freq_dic = defaultdict(int)
    for word in words:
        if word not in stop:
            freq_dic[word]+=1
            vocab[word]+=1
    doc_freq_dic.append(dict(freq_dic))
    # print msgSet
    # break
vocab=dict(vocab)
""" vocab building done """
sorted_vocab = sorted(vocab.items(),key=operator.itemgetter(1))
print sorted_vocab[-50:]
vocabList = [key for key in vocab if vocab[key]>3]
print len(vocabList)


ldaInput = []
for i in range(len(docs)):
    vector = []
    for j in range(len(vocabList)):
        if vocabList[j] in doc_freq_dic[i]:
            vector.append(doc_freq_dic[i][vocabList[j]])
        else:
            vector.append(0)
    vector.append(file_names.index(docs[i][1]))
    ldaInput.append(vector)

ldaInput = np.array(ldaInput)

train_x = ldaInput[:3000,:-1]
train_y = ldaInput[:3000,-1]

test_x = ldaInput[3000:6000,:-1]
test_y = ldaInput[3000:6000,-1]
# print test_y[0]
print train_x.shape,train_y.shape,test_x.shape,test_y.shape

clf = svm.NuSVC()
clf.fit(train_x,train_y)

ans_y = clf.predict(test_x)
TP=0
TN=0
FP=0
FN=0
miss = 0
for i in range(ans_y.shape[0]):
    if ans_y[i] != test_y[i]:
        miss += 1
        print docs[3000+i][0],file_names[test_y[i]],file_names[ans_y[i]]
    if ans_y[i]==0 and test_y[i]==0:
        TN+=1
    if ans_y[i]==1 and test_y[i]==1:
        TP+=1
    if ans_y[i]==0 and test_y[i]==1:
        FN+=1
    if ans_y[i]==1 and test_y[i]==0:
        FP+=1
print "Total misses : " + str(miss)
print 'True Positive: ',TP
print 'False Positive: ',FP
print 'False Negative: ',FN
print 'True Negative: ',TN

print 'Recall: ',(1.0*TP)/(TP+FN)
print 'Precision: ',(1.0*TP)/(TP+FP)


while 1:
    print 'Enter new msg: '
    msg = raw_input()
    msg= re.sub(r'[^\w'+removelist+']', '',msg).lower()
    lmtzr = WordNetLemmatizer()
    words = map(lmtzr.lemmatize,msg.split())
    freq_dic = defaultdict(int)
    for word in words:
        if word not in stop:
            freq_dic[word]+=1
    vector = []
    for j in range(len(vocabList)):
        if vocabList[j] in doc_freq_dic:
            vector.append(doc_freq_dic[vocabList[j]])
        else:
            vector.append(0)
    output = clf.predict(vector)
    print output
    if output==0:
        print 'Sports'
    else:
        print 'Tech'
