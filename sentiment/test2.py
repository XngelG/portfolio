import sentiment_own as sn

data=sn.sentimentCalc('Taylor Swift')
print(data.negative)
print(data.positive)
print(data.neutral)
print(data.wordcloud_neg)
print(data.wordcloud_pos)