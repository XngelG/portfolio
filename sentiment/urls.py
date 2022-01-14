from django.urls import path
from .views import sentimentAPIView

urlpatterns = [
    path('sentiment/', sentimentAPIView.as_view(), name="sentiment"),
]