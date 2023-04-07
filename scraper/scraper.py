# Import needed libraries
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import requests
import cchardet


def parse_bbc():
    url = "https://www.bbc.com"
    response = requests.get(url)
    encoding = cchardet.detect(response.content)['encoding']
    page = response.content.decode(encoding)
    soup = BeautifulSoup(page, 'lxml')
    news_articles = soup.find_all('div', class_='media__content')

    parsed_articles = []

    for article in news_articles[:10]:
        try:
            link = article.find('a')['href']
            if url not in link:  # for links that don't include their domain, only their path such as /news/world-europe-65161095
                link = url + link

            title = article.find('a').get_text(strip=True)

            response = requests.get(link)
            encoding = cchardet.detect(response.content)['encoding']
            page = response.content.decode(encoding)
            soup_article = BeautifulSoup(page, 'lxml')

            author = soup_article.find(
                'div', class_='ssrcss-68pt20-Text-TextContributorName e8mq1e96').get_text().split("By ")[1]
            date = soup_article.find('time')['datetime']
            source = "BBC"
            body = soup_article.find_all(
                'article', class_='ssrcss-pv1rh6-ArticleWrapper e1nh2i2l6')
            x = body[0].find_all('p')

            list_paragraphs = []
            for p in np.arange(0, len(x)):
                paragraph = x[p].get_text()
                list_paragraphs.append(paragraph)
                content = " ".join(list_paragraphs)
            parsed_article = {'Title': title, 'Author': author,
                              'Published Date': date, 'Content': content,
                              'URL': link, 'Source': source}

            parsed_articles.append(parsed_article)
        except Exception as e:
            print("[ERROR] News article parsing error!", e)
    return parsed_articles


def parse_guardian():
    url = "https://www.theguardian.com/"
    r1 = requests.get(url)
    encoding = cchardet.detect(r1.content)['encoding']
    page = r1.content.decode(encoding)
    soup = BeautifulSoup(page, 'lxml')
    news_articles = soup.find_all('div', class_='fc-item__container')
    parsed_articles = []

    for article in news_articles[:10]:
        try:
            link = article.find('a')['href']
            title = article.find(
                'a', class_="u-faux-block-link__overlay js-headline-text").get_text().strip()

            response = requests.get(link)
            encoding = cchardet.detect(response.content)['encoding']
            page = response.content.decode(encoding)
            soup_article = BeautifulSoup(page, 'lxml')

            author = soup_article.find(
                'div', class_='dcr-ub3a78').find('a').get_text()
            date = soup_article.find(
                'summary', class_="dcr-1ybxn6r").get_text()
            date_split = date.split(" ")
            year = date_split[3]
            day = date_split[1]
            month = date_split[2]
            datetime_object = datetime.strptime(month, "%b")
            month_number = datetime_object.month
            date = datetime(year, month_number, day)
            source = "The Guardian"
            body = soup_article.find_all('div', class_='dcr-1ncmr12')
            x = body[0].find_all('p')

            list_paragraphs = []
            for p in np.arange(0, len(x)):
                paragraph = x[p].get_text(strip=True)
                list_paragraphs.append(paragraph)
                content = " ".join(list_paragraphs)

            parsed_article = {'Title': title, 'Author': author,
                              'Published Date': date, 'Content': content,
                              'URL': link, 'Source': source
                              }
            parsed_articles.append(parsed_article)
        except Exception as e:
            print("[ERROR] News article parsing error!", e)
    return parsed_articles


def parse_daily_mail():
    url = "https://www.dailymail.co.uk/"
    r1 = requests.get(url)

    encoding = cchardet.detect(r1.content)['encoding']
    page = r1.content.decode(encoding)
    soup = BeautifulSoup(page, 'lxml')

    news_articles = soup.find_all('h2', class_='linkro-darkred')

    parsed_articles = []

    for article in news_articles[:10]:
        try:
            link = url+article.find('a')['href']
            print(link)
            title = article.find('a').get_text().strip()

            response = requests.get(link)
            encoding = cchardet.detect(response.content)['encoding']
            page = response.content.decode(encoding)
            soup_article = BeautifulSoup(page, 'lxml')

            author = soup_article.find('a', class_='author').get_text()
            date = soup_article.find('time')['datetime']
            source = "Daily Mail"
            body = soup_article.find_all('p', class_='mol-para-with-font')
            x = body[0].find_all('p')

            # Unifying the paragraphs
            list_paragraphs = []
            for p in body:
                paragraph = p.get_text(strip=True)
                list_paragraphs.append(paragraph)
                content = " ".join(list_paragraphs).strip()

            parsed_article = {'Title': title, 'Author': author,
                            'Published Date': date, 'Content': content,
                            'URL': link, 'Source': source
                            }
            parsed_articles.append(parsed_article)
        except Exception as e:
            print("[ERROR] News article parsing error!", e)
    return parsed_articles
