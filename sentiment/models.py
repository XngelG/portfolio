from django.db import models
from .sentiment_own import *

class sentiment(models.Model):
    keyword = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=254,blank=True)
    positive = models.FloatField(null=True, blank=True)
    negative = models.FloatField(null=True, blank=True)
    neutral = models.FloatField(null=True, blank=True)
    wordcloud_neg = models.JSONField(null=True,blank=True) 
    wordcloud_pos = models.JSONField(null=True,blank=True) 

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

class trends(models.Model):
    trend_1 = models.CharField(max_length=30,null=True, blank=True)
    trend_2 = models.CharField(max_length=30,null=True, blank=True)
    trend_3 = models.CharField(max_length=30,null=True, blank=True)
    trend_4 = models.CharField(max_length=30,null=True, blank=True)
    trend_5 = models.CharField(max_length=30,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-created_at',)
    
    def __str__(self):
        return self.trend_1

    def save(self,*args,**kwargs):
        data_trends = fetchTrendingtopics()
        self.trend_1 = data_trends[0]
        self.trend_2 = data_trends[1]
        self.trend_3 = data_trends[2]
        self.trend_4 = data_trends[3]
        self.trend_5 = data_trends[4]

        super().save(*args,**kwargs)
    


