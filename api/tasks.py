import time
from celery import shared_task
import requests


@shared_task
def parse_summarize_articles(self, request):
    response = requests.post('http://127.0.0.1:8000/api/articles/')
    return "Success"
