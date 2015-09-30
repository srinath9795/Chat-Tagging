# -*- coding: utf-8 -*-
import re
dic = {
"aren't":"are not",
"can’t":"can not",
"could’ve":"could have",
"couldn’t":"could not",
"couldn’t’ve":"could not have",
"didn’t":"did not",
"doesn’t":"does not",
"don’t":"do not",
"hadn’t":"had not",
"hadn’t’ve":"had not have",
"hasn’t":"has not",
"haven’t":"have not",
#"he’d":"he had / he would",
"he’d":"he had",
"he’d’ve":"he would have",
#"he’ll":"he shall / he will",
"he’ll":"he will",
#"he’s":"he has / he is",
"he’s":"he is",
#"how’d":"how did / how would",
"how’ll":"how will",
#"how’s":"how has / how is / how does",
#"I’d":"I had / I would",
"I’d’ve":"I would have",
#"I’ll":"I shall / I will",
"I’m":"I am",
"I’ve":"I have",
"isn’t":"is not",
#"it’d":"it had / it would",
"it’d":"it would",
"it’d’ve":"it would have",
#"it’ll":"it shall / it will",
"it’ll":" it will",
#"it’s":"it has / it is",
"it’s":"it is",
"let’s":"let us",
"ma’am":"madam",
"mightn’t":"might not",
"mightn’t’ve":"might not have",
"might’ve":"might have",
"mustn’t":"must not",
"must’ve":"must have",
"needn’t":"need not",
"not’ve":"not have",
"o’clock":"of the clock",
"oughtn’t":"ought not",
"shan’t":"shall not",
#"she’d":"she had / she would",
"she’d":"she would",
"she’d’ve":"she would have",
#"she’ll":"she shall / she will",
"she’ll":"she will",
#"she’s":"she has / she is",
"she’s":"she is",
"should’ve":"should have",
"shouldn’t":"should not",
"shouldn’t’ve":"should not have",
#"somebody’d":"somebody had / somebody would",
"somebody’d":"somebody would",
"somebody’d’ve":"somebody would have",
#"somebody’ll":"somebody shall / somebody will",
"somebody’ll":"somebody will",
#"somebody’s":"somebody has / somebody is",
#"someone’d":"someone had / someone would",
"someone’d":"someone would",
"someone’d’ve":"someone would have",
#"someone’ll":"someone shall / someone will",
"someone’ll":"someone will",
#"someone’s":"someone has / someone is",
#"something’d":"something had / something would",
"something’d":"something would",
"something’d’ve":"something would have",
#"something’ll":"something shall / something will",
"something’ll":"something will",
"something’s":"something has / something is",
"that’ll":"that will",
#"that’s":"that has / that is",
"there’d":"there had / there would",
"there’d’ve":"there would have",
"there’re":"there are",
#"there’s":"there has / there is",
#"they’d":"they had / they would",
"they’d’ve":"they would have",
#"they’ll":"they shall / they will",
"they’re":"they are",
"they’ve":"they have",
"’twas":"it was",
"wasn’t":"was not",
#"we’d":"we had / we would",
"we’d":"we would",
"we’d’ve":"we would have",
"we’ll":"we will",
"we’re":"we are",
"we’ve":"we have",
"weren’t":"were not",
#"what’ll":"what shall / what will",
"what’ll":"what will",
"what’re":"what are",
#"what’s":"what has / what is / what does",
"what’s":"what is",
"what’ve":"what have",
#"when’s":"when has / when is",
"when’s":"when is",
"where’d":"where did",
#"where’s":"where has / where is",
"where’s":"where is",
"where’ve":"where have",
#"who’d":"who would / who had",
"who’d":"who would",
"who’d’ve":"who would have",
#"who’ll":"who shall / who will",
"who’ll":"who will",
"who’re":"who are",
#"who’s":"who has / who is",
"who’ve":"who have",
"why’ll":"why will",
"why’re":"why are",
#"why’s":"why has / why is",
"why’s":"why is",
"won’t":"will not",
"would’ve":"would have",
"wouldn’t":"would not",
"wouldn’t’ve":"would not have",
"y’all":"you all",
"y’all’ll":"you all will",
#"y’all’d’ve":"you all should have / you all could have / you all would have",
#"you’d":"you had / you would",
"you’d":"you would",
"you’d’ve":"you would have",
#"you’ll":"you shall / you will",
"you’ll":"you will",
"you’re":"you are",
"you’ve":"you have"
}

def normalize(s):
	for x in dic.keys():
		s=s.replace(x,dic[x])
	#print(type(s))
	s=s.replace("'s",'')
	s=re.sub(r'[,\(\)\[\]\{\}]',' ',s)
	s=re.sub(r'[^a-zA-Z\d\s\.]', '', s)
	return s

if __name__ == '__main__':
	with open('./reddit_data/technology.txt') as data_file:    
		count=0
		for line in data_file:
			count+=1
			print(line)
			print(replace_contraction(line))
			if(count==1000):
				exit()

	







