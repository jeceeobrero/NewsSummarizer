# Web Scraper

This scraper parses three reputable sources namely, BBC, The Guardian, and Daily Mail. It mainly uses Newspaper3k to acquire information from a browser that is HTML rendered
and uses Beautiful Soup to extract few information from Javascript rendered pages. 

## How it Works

1) Set first the config for the news article parsing. 
```
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10
```
2) Call each news paper source to parse to store their corresponding parsed articles.
```
parsed_bbc = parse_bbc(config)
parsed_guardian = parse_guardian(config)
parsed_daily_mail = parse_daily_mail(config)
```
3) In each parse function, you have to set the news source url and build the newspaper. In order not to parse articles that were parsed before, you set the memoize_articles to be True. This prevents duplicate querying for a given article and can save resources. Note also that article_urls are of type set in order to not store duplicate urls.
```
news_source_url = 'https://www.bbc.com'
article_urls = set()
bbc = newspaper.build(news_source_url, config=config, memoize_articles=False, language='en')
```
3) Initialize the  parsed_articles.
```
 parsed_articles = []
```
4) Parsed for the article information such as title, author, URL, and source. We use Newspaper3k in this one. Newspaper3k is very useful in this one since we don't have to parse thru the news source's HTML which sometimes might change. Thus, this is much safer and secured way to get information.
```
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
            article_title = article.title
            print(article.title)
            article_meta_data = article.meta_data
```
5) Sometimes Newspaper3k can't read some of the information. That's why we have to parse now for other remaining information such as author using Beautiful Soup.
```
            soup = BeautifulSoup(article.html, 'html.parser')
            bbc_dictionary = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))
            # print(bbc_dictionary)

            date_published = [value for (key, value) in bbc_dictionary.items() if key == 'datePublished']
            print(date_published)

            soup_article = BeautifulSoup(article.html, 'lxml')
            article_author = soup_article.find('div', class_='ssrcss-68pt20-Text-TextContributorName e8mq1e96').get_text().split("By ")[1]
            article_author = article_author if article_author else "BBC"
            print(article_author)
            article_text = soup_article.find_all(
                        'article', class_='ssrcss-pv1rh6-ArticleWrapper e1nh2i2l6')
            x = article_text[0].find_all('p')
            
            # Combine all paragraphs 
            list_paragraphs = []
            for p in np.arange(0, len(x)):
                paragraph = x[p].get_text()
                list_paragraphs.append(paragraph)
                article_text = " ".join(list_paragraphs)
```
6) We have extracted the required data which are title, author, content, published date, source, and lastly, URL.
```
            parsed_article = {
                'Title': article_title,
                'Author': article_author,
                'Published Date': date_published,
                'Source': "BBC",
                "URL": sub_article.url,
                "Content": article_text
            }
            print(parsed_article)
            parsed_articles.append(parsed_article)
```
7) If there are any errors in parsing and in extracting data, an error log is displayed. We take not of errors such as ArticleException and MaxRetryError, and if ever there are other errors, we catch them with an Exception.
```
    except ArticleException as e:
        print("Article not found. ")
    except MaxRetryError as e:
        print("Failed to connect to the website. Please check your internet connection.")
    except Exception as e:
        # Handle the exception
        print(f"An error occurred: {e}")
```
8) The parsed articles will be returned as it will used for future processing which is the summary.
```
return parsed_articles
```
9) Combine all parsed articles and return it.
```
    parsed_bbc = parse_bbc(config)
    parsed_guardian = parse_guardian(config)
    parsed_daily_mail = parse_daily_mail(config)
    
    parsed_articles = []
    parsed_articles.extend(parsed_bbc) 
    parsed_articles.extend(parsed_guardian)
    parsed_articles.extend(parsed_daily_mail)
    
    return parsed_articles    
```