from django.urls import path
from .views import NewsArticleList

urlpatterns = [
    path('articles/', NewsArticleList.as_view(), name='article-list')
]