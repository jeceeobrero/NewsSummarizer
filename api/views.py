from django.core.cache import cache
from .models import NewsArticle
from .serializers import NewsArticleSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from scraper.scraper import parse_news_sources
from summarizer.summarizer import generate_summary
from django.db import transaction
from datetime import datetime, timedelta
from .tasks import parse_summarize_articles
class NewsArticlePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class NewsArticleList(APIView):
    pagination_class = NewsArticlePagination

    @transaction.atomic
    def post(self, request):
        # Get the parsed articles from BBC, The Guardian, Daily Mail
        parsed_articles = parse_news_sources()
        print(parsed_articles)
        try:
            for article in parsed_articles:
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
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        # Retrieve all NewsArticle objects from the database
        news_articles = NewsArticle.objects.all().order_by('-published_date')

        # Paginate the NewsArticle objects
        paginator = Paginator(news_articles, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Serialize the NewsArticle objects
        serializer = NewsArticleSerializer(page_obj, many=True)

        # Return the serialized NewsArticle objects as a JSON response
        return Response({"news_articles": serializer.data, "page_number": page_obj.number, "total_pages": paginator.num_pages}, status=status.HTTP_200_OK)
    

class NewsArticleTask(APIView):
    def post(self, request):
        eta = datetime.now() + timedelta(hours=1)
        parse_summarize_articles.apply_async(args=[4, 4], eta=eta)