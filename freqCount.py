from collections import defaultdict
from nltk.corpus import stopwords
import enchant

d = enchant.Dict("en_US")
print d.suggest("li8")
print d.suggest("g2g")
print d.suggest("twomoro")






# stop = stopwords.words('english')
# print stop



# words = "this is this is awesome lol"
# words = words.split()
# total = 0
# count = defaultdict(lambda: 0)
# for word in words:
#     total += 1
#     count[word] += 1

# Now you can just determine the frequency by dividing each count by total
# for word, ct in count.items():
#      print('Frequency of %s: %f%%' % (word, 100.0 * float(ct) / float(total)))