# Import needed libraries
import json
import newspaper
from newspaper import Config
from newspaper import Article, ArticleException
from newspaper.utils import BeautifulSoup
from urllib3.exceptions import MaxRetryError
import numpy as np


def parse_news_sources():
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

    config = Config()
    config.browser_user_agent = USER_AGENT
    config.request_timeout = 10

    # Call all news sources to parse 
    parsed_bbc = parse_bbc(config)
    parsed_guardian = parse_guardian(config)
    parsed_daily_mail = parse_daily_mail(config)
    
    parsed_articles = []
    parsed_articles.extend(parsed_bbc) 
    parsed_articles.extend(parsed_guardian)
    parsed_articles.extend(parsed_daily_mail)
    
    return parsed_articles    

def parse_bbc(config):
    news_source_url = 'https://www.bbc.com'
    article_urls = set()
    bbc = newspaper.build(news_source_url, config=config, memoize_articles=True, language='en')
    
    parsed_articles = []
    
    for sub_article in bbc.articles:
        if sub_article.url not in article_urls:
            try:
                article_urls.add(sub_article.url)
                article = Article(sub_article.url, config=config, memoize_articles=True, language='en')
                article.download()
                article.parse()

                # The majority of the article elements are located
                # within the meta data section of the page's
                # navigational structure
                
                # Get title
                article_title = article.title

                soup = BeautifulSoup(article.html, 'html.parser')
                bbc_dictionary = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))

                # Get date
                date_published = [value for (key, value) in bbc_dictionary.items() if key == 'datePublished']
                
                soup_article = BeautifulSoup(article.html, 'lxml')
                
                # Get Author
                if(None==soup_article.find('div', class_='ssrcss-68pt20-Text-TextContributorName e8mq1e96').get_text().split("By ")[1]):
                    article_author = "BBC"
                else:
                    article_author = soup_article.find('div', class_='ssrcss-68pt20-Text-TextContributorName e8mq1e96').get_text().split("By ")[1]
                    
                # Get article text
                article_text = soup_article.find_all(
                            'article', class_='ssrcss-pv1rh6-ArticleWrapper e1nh2i2l6')
                x = article_text[0].find_all('p')

                list_paragraphs = []
                for p in np.arange(0, len(x)):
                    paragraph = x[p].get_text()
                    list_paragraphs.append(paragraph)
                    article_text = " ".join(list_paragraphs)
                
                parsed_article = {
                    'Title': article_title,
                    'Author': article_author,
                    'Published Date': date_published,
                    'Source': "BBC",
                    "URL": sub_article.url,
                    "Content": article_text
                }
                parsed_articles.append(parsed_article)
            except ArticleException as e:
                print("Article not found. ")
            except MaxRetryError as e:
                print("Failed to connect to the website. Please check your internet connection.")
            except Exception as e:
                # Handle the exception
                print(f"An error occurred: {e}")
    return parsed_articles


def parse_guardian(config):
    news_source_url = 'https://www.theguardian.com/'
    article_urls = set()
    news_source = newspaper.build(news_source_url, config=config, memoize_articles=True, language='en')

    parsed_articles = []

    # Go immediately to the articles, article[0:7] are only index htmls and not valid articles
    for sub_article in news_source.articles:
        if sub_article.url not in article_urls:
            try:
                article_urls.add(sub_article.url)
                article = Article(sub_article.url, config=config, memoize_articles=True, language='en')
                article.download()
                article.parse()

                # The majority of the article elements are located
                # within the meta data section of the page's
                # navigational structure
                # the replace is used to remove newlines
                
                # Get article text
                article_text = article.text.replace('\n', '')
                
                # Get title
                article_title = article.title
                article_meta_data = article.meta_data

                # Get date
                date_published = article_meta_data['article']['published_time']
                soup= BeautifulSoup(article.html, 'lxml')
                
                # Get author
                if (None==soup.find('div', class_='dcr-172h0f2').find('a').get_text()):
                    article_author = "The Guardian"
                else:
                    article_author = soup.find('div', class_='dcr-172h0f2').find('a').get_text()

                parsed_article = {
                    'Title': article_title,
                    'Author': article_author,
                    'Published Date': date_published,
                    'Source': "The Guardian",
                    "URL": sub_article.url,
                    "Content": article_text
                }
                parsed_articles.append(parsed_article)
            except ArticleException as e:
                print("Article not found. ")
            except MaxRetryError as e:
                print("Failed to connect to the website. Please check your internet connection.")
            except Exception as e:
                # Handle the exception
                print(f"An error occurred: {e}")
    return parsed_articles


def parse_daily_mail(config):
    news_source_url = 'https://www.dailymail.co.uk/home/index.html'
    article_urls = set()
    news_source = newspaper.build(
        news_source_url, config=config, memoize_articles=True, language='en')

    parsed_articles = []

    # Go immediately to the articles, article[0:7] are only index htmls and not valid articles
    for sub_article in news_source.articles:
        if sub_article.url not in article_urls:
            try:
                article_urls.add(sub_article.url)
                article = Article(sub_article.url, config=config,
                                memoize_articles=True, language='en')
                article.download()
                article.parse()

                # The majority of the article elements are located
                # within the meta data section of the page's
                # navigational structure
                # the replace is used to remove newlines
                
                # Get article text
                article_text = article.text.replace('\n', '')
                
                # Get title
                article_title = article.title
                article_meta_data = article.meta_data
                
                # Get date
                date_published = article_meta_data['article']['published_time']
                
                # Get author
                article_author = article_meta_data['author']
                article_author = article_author if article_author else "Daily Mail"
                
                parsed_article = {
                    'Title': article_title,
                    'Author': article_author,
                    'Published Date': date_published,
                    'Source': "Daily Mail",
                    "URL": sub_article.url,
                    "Content": article_text
                }
                parsed_articles.append(parsed_article)
            except ArticleException as e:
                print("Article not found. ")
            except MaxRetryError as e:
                print("Failed to connect to the website. Please check your internet connection.")
                parse_daily_mail()
            except Exception as e:
                # Handle the exception
                print(f"An error occurred: {e}")
    return parsed_articles
