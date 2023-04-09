from django.urls import path
from .views import NewsArticleList, NewsArticleTask

urlpatterns = [
    path('articles/', NewsArticleList.as_view(), name='article-list'),
    path('tasks/', NewsArticleTask.as_view(), name='article-task')
]