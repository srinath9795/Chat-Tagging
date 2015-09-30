from collections import defaultdict
import MySQLdb as mdb
import time
from nltk.corpus import stopwords


con=mdb.connect('localhost','root','pass','sms')
cur=con.cursor()

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
	arr_list=getindices(len(a)-1,len(b)-1)
	ret=None

	mpr=0
	for arr in arr_list:
		pr=1
		for ind in range(len(arr)):
			if ind==0:
				pr*=probc(a[ind],b[0:arr[ind]],data)
			else:
				pr*=probc(a[ind],b[arr[ind-1]:arr[ind]],data)
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

d=learn(cur.fetchall())





stop=stopwords.words('english')
stop.append('awesome')
wp=list()
for word in stop:
	r=probw('awsum',word,d)
	wp.append((word,r))


wp=sorted(wp,key=lambda x: x[1])

print wp
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