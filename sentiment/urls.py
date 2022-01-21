from django.urls import path
from .views import sentimentAPIView, trendsAPIView

urlpatterns = [
    path('sentiment/', sentimentAPIView.as_view(), name="sentiment"),
    path('trends/', trendsAPIView.as_view(), name="trends"),
]