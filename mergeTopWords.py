file_names = ['sports','technology','movies','music','politics','programming']

print 'class\tword\tcount'
for fn in file_names:
	f = open('reddit_top_words/'+fn,'r')
	for line in f:
		line = line.strip().split()
		print fn+'\t'+line[0]+'\t'+line[1]
		# break
	# tmp = [(l.split()[0],int(l.split()[1])) for l in f]
	# top_words_dict[fn] = dict(tmp)
	f.close()