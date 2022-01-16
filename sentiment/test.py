import sentiment_own as sn


data = sn.sentimentCalc('fnatic')
print(data.positive)
print(data.negative)
print(data.neutral)
print(data.wordcloud_neg)
print(data.wordcloud_pos)
