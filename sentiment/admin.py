from django.contrib import admin
from .models import sentiment,trends

class sentimentModelAdmin(admin.ModelAdmin):
    list_display = ('keyword','created_at','email')
    search_fields = ('keyword',)
    list_per_page = 10

class trendsModelAdmin(admin.ModelAdmin):
    list_display = ('trend_1','created_at')
    search_fields = ('trend_1','trend_2','trend_3','trend_4','trend_5',)
    list_per_page = 10



admin.site.register(sentiment,sentimentModelAdmin)
admin.site.register(trends,trendsModelAdmin)