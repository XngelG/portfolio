from django.contrib import admin
from .models import sentiment

class sentimentModelAdmin(admin.ModelAdmin):
    list_display = ('keyword','created_at','email')
    search_fields = ('keyword',)
    list_per_page = 10

admin.site.register(sentiment,sentimentModelAdmin)