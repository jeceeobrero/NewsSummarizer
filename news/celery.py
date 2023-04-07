import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

broker = 'sqla+postgresql://postgres:GSsNudgrToko9ai86QOz@containers-us-west-51.railway.app/railway'

app = Celery('news')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)
