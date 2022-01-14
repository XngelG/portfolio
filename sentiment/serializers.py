from rest_framework import serializers
from .models import sentiment

class sentimentSerializer(serializers.ModelSerializer):

    class Meta:
        model = sentiment
        fields = "__all__"