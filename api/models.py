from django.db import models

class NewsArticle(models.Model):
    url = models.CharField(max_length=255, unique=True)
    title = models.TextField(max_length=255)
    author = models.TextField(max_length=255)
    published_date = models.DateTimeField()
    parsed_content = models.TextField()
    summarized_content = models.TextField(null=True)
    source = models.TextField()
    
    def __str__(self):
        return self.title