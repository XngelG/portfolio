from django.shortcuts import render
from rest_framework import generics,response,status
from .models import sentiment,trends
from .serializers import sentimentSerializer,trendsSerializer

class sentimentAPIView(generics.CreateAPIView):
    serializer_class=sentimentSerializer

    def get_queryset(self):
        return sentiment.objects.all()

class trendsAPIView(generics.CreateAPIView):
    serializer_class=trendsSerializer

    def get_queryset(self):
        return trends.objects.all()
