from collections import defaultdict
import MySQLdb as mdb
import nltk
from nltk.corpus import stopwords
from nltk.corpus import words
from nltk import word_tokenize
import enchant
import threading
import string
# import flask
# from flask import request,Flask
# import json

from nltk.corpus import brown

con=mdb.connect('localhost','root','mandava','sms')
cur=con.cursor()

cfreq_brown_2gram = nltk.ConditionalFreqDist(nltk.bigrams(brown.words()))

english_dictionary = enchant.Dict("en_US")

# app=Flask(__name__)

print type(cfreq_brown_2gram)
def permute(p,l,m,r=None):
	r=[] if r is None else r
	if l==[]:
		r.append(p)
	else:
		s=None
		e=None
		if p==[]:
			s=1
			e=m-len(l)+1
		else:
			s=p[-1]+1
			e=m-len(l)+1
		for i in xrange(s,e+1):
			permute(p+[i],l[1:],m,r)

def getindices(length,m):
	l=[i for i in range(length)]
	result=[]
	permute([],l,m,result)
	return result

def pairs(a,b,data,c=1):
	a='$'+a+'$'
	b='$'+b+'$'

	arr_list=getindices(len(a)-1,len(b)-1)
	# print arr_list
	ret=[]
	for arr in arr_list:
		for i in range(len(arr)):
			if i==0:
				s=b[0:arr[i]]
			else:
				s=b[arr[i-1]:arr[i]]
			# if str(a[i])!=s:
				# print arr[i],s,a[i]
			ret.append((a[i],s))
		ret.append((a[-1],b[arr[-1]:]))
	
	for a,b in ret:
		if b in data:
			for d in data[b]:
				if d[0]==a:
					d[1]+=1*c
					break
			else:
				data[b].append([a,1*c])
		else:
			data[b]=list()
			data[b].append([a,1*c])

	# print data
	return ret

def probc(a,b,data):
	c=0
	
	for d in data[b]:
		c+=d[1]
	for d in data['$'+b]:
		c+=d[1]
	for d in data[b+'$']:
		c+=d[1]

	if set(a)==set(b) and len(set(a))==1:
		# if len(b)>1:
		# 	print a,b
		return 1.0/len(b)*1.0

	for d in data[b]:
		if d[0]==a:
			return d[1]/float(c)
	for d in data[b+'$']:
		if d[0]==a:
			return d[1]/float(c)

	for d in data['$'+b]:
		if d[0]==a:
			return d[1]/float(c)

	
	return 0


def probw(a,b,data):
	a='$'+a+'$'
	b='$'+b+'$' 
	if len(a)>len(b):
		a,b=b,a
	arr_list=getindices(len(a)-1,len(b)-1)
	# ret=None

	mpr=0
	for arr in arr_list:
		pr=1
		for ind in range(len(arr)):
			if ind==0:
				pr*=probc(a[ind],b[0:arr[ind]],data)
			else:
				pr*=probc(a[ind],b[arr[ind-1]:arr[ind]],data)
			if pr<mpr:
				break
		if pr>mpr:
			mpr=pr

	return mpr




def learn(rows):
	d=defaultdict(lambda:[])
	# print len(rows)
	for a,b,c in rows:
		pairs(a,b,d,int(c))
		# print len(d.items())
	return d


# print probc('$','to',d),probc('t','to',d)
# print d['$to']

cur.execute("select * from norm")
b=cur.fetchall()
d=learn(b)
translationMap = {}
vocab = {}
for a in b:
	translationMap[a[0]]=a[1]
	vocab[a[1]]=1
vocab=vocab.keys()
englishVocab = words.words()
translationMap['der']='there'
translationMap['dis']='this'
translationMap['2']='to'
translationMap['plsss']='please'
stop=stopwords.words('english')


estimate_list_vars=[]

def estimate_list(tn,token,l,d,dfval=1):
	wp=[]
	for word in l:
		# print 'checking '+ ptoken+ ' for ',word	
		if len(word)==1:
			continue
		r=probw(token,word,d)*dfval
		wp.append((word,r))
	# estimate_list_vars[tn]=wp
	return wp

def normalize(sms):
	tokens = word_tokenize(sms)
	print tokens
	translated = []
	i=0
	for token in tokens:
		if token in string.punctuation:
			translated.append(token)
		elif english_dictionary.check(token) and (len(token) is not 1 or token is 'i' or token is 'a' or token is 'I' or token is 'A'):
			print 'already present in english dictionary ', token
			translated.append(token)

		elif token in translationMap:
			# print 'already present in map ',token,translationMap[token]
			translated.append(translationMap[token])
			
		else:
			wp=list()
			global estimate_list_vars
			if i==0:
				# for word in vocab:
				# 	r=probw(token,word,d)
				# 	wp.append((word,r))
				wp=estimate_list(0,token,vocab,d)
				wp+=estimate_list(1,token,english_dictionary.suggest(token),d,10)

			else:
				# model_poss=cfreq_brown_2gram[ptoken].items()
				# model_poss.sort(key=lambda x:x[1])
				# model_poss=[m[0] for m in model_poss[:100]]
				model_poss=[]

				mthreads=2
				estimate_list_vars=[[] for n in range(mthreads+1)]
				# anthrad=threading.Thread(target=estimate_list,
				#     	args=(mthreads,token,model_poss,d,))
				# anthrad.start()
				# threads=[]
				# for z in range(mthreads):
				#     t = threading.Thread(target=estimate_list,
				#     	args=(z,token,vocab[z*len(vocab)/mthreads:(z+1)*len(vocab)/mthreads],d,))
				#     threads.append(t)
				#     t.start()

				# for word in model_poss +vocab[0:len(vocab)/10]:
				# 	# print 'checking '+ ptoken+ ' for ',word	
				# 	r=probw(token,word,d)
				# 	wp.append((word,r))
				# for thread in threads:
				# 	thread.join()
				# # anthrad.join()
				# for z in estimate_list_vars:
				# 	# print z
				# 	wp+=z
				# 	print z[-10:]

				wp=estimate_list(0,token,vocab,d)
				wp+=estimate_list(1,token,english_dictionary.suggest(token),d,10)

				
			wp=sorted(wp,key=lambda x: x[1])
			#print 'norm done',token,wp[-1][0]
			print wp[-5:]
			translated.append(wp[-1][0])
		i+=1
		ptoken=translated[-1]
	return ' '.join(translated)


# print probc("2moro","tomorrow",d)
# for i in range(ord('a'),ord('z')):
# 	print chr(i),probc(chr(i),chr(i),d)




# d=defaultdict(lambda:[])
# pairs('moro','tomorrow',d)
# pairs('2moro','tomorrow',d)
# pairs('tomo','tomorrow',d)
# pairs('tom','tomorrow',d)
# pairs('2mro','tomorrow',d)


# print "d['to']",d['to']
# print "d['$to']",d['$to'],d['t']
# print d['morro']

print 'ready '

import re
regex = r'(.)\1{3}'
pattern=re.compile(regex)

while True:

	inm=raw_input()
	while pattern.search(inm) is not None:
		a,b=pattern.search(inm).span()
		inm=inm[0:a]+2*inm[a]+inm[b:]


	print normalize(inm)

# hw on erth iz tht posibl
# tmrw i wil do exrcse
# tht ws a gr8 game
# pls arve on time
# prvius  verson is lxicogrphicly smaller
# all posble prdcts wid four difrnt featurs
