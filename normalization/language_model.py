####
# reference http://www.katrinerk.com/courses/python-worksheets/language-models-in-python
####


import nltk

from nltk.corpus import brown


import string
import sys

# complain if we didn't get a filename
# as a command line argument
if len(sys.argv) < 2:
    print "Please enter the name of a corpus file as a command line argument."
    sys.exit()


    
# try opening file 
# If the file doesn't exist, catch the error
try:
    f = open(sys.argv[1])
except IOError:
    print "Sorry, I could not find the file", sys.argv[1]
    print "Please try again."
    sys.exit()
    
# read the contents of the whole file into ''filecontents''
filecontents = f.read()
        
# count bigrams 
bigrams = {} 
words_punct = filecontents.split() 
# strip all punctuation at the beginning and end of words, and 
# convert all words to lowercase.
# The following is a Python list comprehension. It is a command that transforms a list,
# here words_punct, into another list.
words = [ w.strip(string.punctuation).lower() for w in words_punct ]





# an nltk.FreqDist() is like a dictionary,
# but it is ordered by frequency.
# Also, nltk automatically fills the dictionary
# with counts when given a list of words.

freq_brown = nltk.FreqDist(words)




# an nltk.ConditionalFreqDist() counts frequencies of pairs.
# When given a list of bigrams, it maps each first word of a bigram
# to a FreqDist over the second words of the bigram.

cfreq_brown_2gram = nltk.ConditionalFreqDist(nltk.bigrams(words))





while True:
	x=raw_input()
	# print cfreq_brown_2gram["language"]

	i=0
	for x,fre in cfreq_brown_2gram[x].items():
	# if i<10 and fre>5:
		# i+=1
		print x,fre







