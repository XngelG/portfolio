import sentiment_own as sn


data = sn.sentimentCalc('Donald Trump',1)
print(data.positive)
print(data.negative)
print(data.neutral)
