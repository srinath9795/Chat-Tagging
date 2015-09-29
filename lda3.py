import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
from nltk.stem.wordnet import WordNetLemmatizer
import numpy as np
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
jf = open('item.json')
items = json.load(jf)
cnt = 0
docs = []
tmp = ""
prev = 0
for i in items:
    tmp += i["message"]+" "
    cnt+=1
    if cnt>=5 and i["nick"]!=prev:
        docs += [tmp]
        tmp = ""
        cnt = 0
    prev = i["nick"]

removelist = "=& "  # for non-alpha numeric chars that are allowed
msgCount = 0
doc_freq_dic = []
vocab = defaultdict(int)
stop = stopwords.words('english')
for msgSet in docs:
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
vocabList = [key for key in vocab if vocab[key]>1]
# for key in vocab:
#   if vocab[key]>1:
#       vocabList.append(key)
# sorted_x = sorted(vocab.items(), key=operator.itemgetter(1))
# print sorted_x
print len(vocabList)






ldaInput = []
for i in range(len(docs)):
    vector = []
    for j in range(len(vocabList)):
        if vocabList[j] in doc_freq_dic[i]:
            vector.append(doc_freq_dic[i][vocabList[j]])
        else:
            vector.append(0)
    ldaInput.append(vector)
ldaInput = np.array(ldaInput)
model = lda.LDA(n_topics=20, n_iter=500, random_state=1)
model.fit(ldaInput)
topic_word = model.topic_word_
for n in range(5):
    sum_pr = sum(topic_word[n,:])
    print("topic: {} sum: {}".format(n, sum_pr))
n = 10
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocabList)[np.argsort(topic_dist)][:-(n+1):-1]
    print('*Topic {}\n- {}'.format(i, ' '.join(topic_words)))