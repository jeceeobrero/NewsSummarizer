from django.core.cache import cache
from .models import NewsArticle
from .serializers import NewsArticleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from scraper.scraper import parse_bbc, parse_guardian, parse_daily_mail
from summarizer.summarizer import generate_summary
from django.db import transaction
from celery import shared_task
from datetime import datetime, timedelta
from celery import Celery
class NewsArticleList(APIView):
    @shared_task
    @transaction.atomic
    def post(self, request):
        # Get the parsed articles from BBC, The Guardian, Daily Mail
        bbc_articles = parse_bbc()
        guardina_articles = parse_guardian()
        daily_mail_articles = parse_daily_mail()
        
        news_articles = parse_bbc()
        news_articles.extend(guardina_articles) if guardina_articles else []
        news_articles.extend(daily_mail_articles) if daily_mail_articles else []
        
        try:
            for article in news_articles:
                # Extract all article details
                title = article.get('Title')
                author = article.get('Author')
                published_date = article.get('Published Date')
                parsed_content = article.get('Content')
                source = article.get('Source')
                
                # Check if the news article has already been scraped
                url = article.get('URL')
                cache_key = f'news_article_{url}'
                news_article = cache.get(cache_key)

                # If not yet in cache and db, generate its summary and add to DB. Else, no need to parse and summarize it again.
                if news_article is None:
                    try:
                        news_article = NewsArticle.objects.get(url=url)
                    except NewsArticle.DoesNotExist:
                        # Summarize the parsed content using your machine learning script
                        summarized_content = generate_summary(article)

                        # Create a NewsArticle object and save it to the database
                        news_article = NewsArticle(
                            url=url,
                            title=title,
                            author=author,
                            published_date=published_date,
                            parsed_content=parsed_content,
                            summarized_content=summarized_content,
                            source=source
                        )
                        print(news_article)
                        news_article.save()

                        # Cache the news article for future requests
                        cache.set(cache_key, news_article)
                    
            # Return the serialized NewsArticle object as a JSON response
            return Response("Success")
        except Exception as e:
            return Response("Error: ", e)
    post.delay(*arg, **kwargs)
    def get(self, request):
        eta = datetime.utcnow() + timedelta(hour=1)
        self.post.apply_async(args=[self, request], eta=eta)
        # Retrieve all NewsArticle objects from the database
        news_articles = NewsArticle.objects.all().order_by('-published_date')

        # Serialize the NewsArticle objects
        serializer = NewsArticleSerializer(news_articles, many=True)

        # Return the serialized NewsArticle objects as a JSON response
        return Response({"news_articles": serializer.data})