from django.shortcuts import render
from rest_framework import generics,response,status
from .models import sentiment
from .serializers import sentimentSerializer

class sentimentAPIView(generics.CreateAPIView):
    serializer_class=sentimentSerializer

    def get_queryset(self):
        return sentiment.objects.all()
