from django.db import models
from .sentiment_own import *

class sentiment(models.Model):
    keyword = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=254,blank=True)
    positive = models.FloatField(null=True, blank=True)
    negative = models.FloatField(null=True, blank=True)
    neutral = models.FloatField(null=True, blank=True)
    wordcloud_neg = models.TextField(null=True,blank=True) 
    wordcloud_pos = models.TextField(null=True,blank=True) 

    class Meta:
        ordering=('-created_at',)
    
    def __str__(self):
        return self.keyword
    
    def save(self,*args,**kwargs):
        data_sentiment = sentimentCalc(self.keyword)
        self.positive = data_sentiment.positive
        self.negative = data_sentiment.negative
        self.neutral = data_sentiment.neutral
        self.wordcloud_neg = data_sentiment.wordcloud_neg
        self.wordcloud_pos = data_sentiment.wordcloud_pos

        super().save(*args,**kwargs)
    


