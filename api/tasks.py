import time
from celery import shared_task
import requests


@shared_task
def parse_summarize_articles(self, request):
    response = requests.post('https://nlpnewsummarizer.azurewebsites.net/api/articles/')
    return "Success"
