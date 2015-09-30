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
docs = []
tmp = ""

for fn in file_names:
    jf = open('reddit_data/'+fn,'r')
    for i in jf:
        tmp += i+" "
        cnt+=1
        if cnt==5:
            docs += [(tmp,fn)]
            tmp = ""
            cnt = 0
""" File reading done """
print len(docs)
docs = np.array(docs)
np.random.shuffle(docs)
docs = docs[:6000,:]

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
            freq_dic[word]=1
            vocab[word]+=1
    doc_freq_dic.append(dict(freq_dic))
    # print msgSet
    # break
vocab=dict(vocab)
""" vocab building done """

vocabList = [key for key in vocab if vocab[key]>1]
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

print train_x.shape,train_y.shape,test_x.shape,test_y.shape

clf = svm.SVC()
clf.fit(train_x,train_y)

ans_y = clf.predict(test_x)

miss = 0
for i in range(ans_y.shape[0]):
    if ans_y[i] != test_y[i]:
        miss += 1
        print docs[3000+i][0],file_names[test_y[i]],file_names[ans_y[i]]
print "Total misses : " + str(miss)



