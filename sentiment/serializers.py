from rest_framework import serializers
from .models import sentiment,trends

class sentimentSerializer(serializers.ModelSerializer):

    class Meta:
        model = sentiment
        fields = "__all__"

class trendsSerializer(serializers.ModelSerializer):

    class Meta:
        model = trends
        fields = "__all__"