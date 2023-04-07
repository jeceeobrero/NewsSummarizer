# Web Scraper

This scraper parses three reputable sources namely, BBC, The Guardian, and Daily Mail. It uses Beautiful Soup, one of the popular web scraper libraries. 

## How it Works

1) It defines the news source site and navigates to it.
```
url = "https://www.bbc.com"
```
2) It then determines the encoding of the response content for faster process of parsing using Beautiful Soup.
```
response = requests.get(url)
```
3) Next, it saves the content and is parsed by 'lxml' of Beautiful Soup.
```
page = response.content.decode(encoding)
soup = BeautifulSoup(page, 'lxml')
```
4) The content contains the articles available in that page and since the information we have are only the titles and the links to the article itself, we then need to navigate to it and store the parsed articles in the parsed_articles variable.
```
news_articles = soup.find_all('div', class_='media__content')
parsed_articles = []
```
5) We iterate through the list of articles and do the same process of parsing it with Beautiful Soup. Get the content or paragraphs of each article.
```
for article in news_articles:
    try:
        link = article.find('a')['href']
        if url not in link:  # for links that don't include their domain, only their path such as /news/world-europe-65161095
            link = url + link
        title = article.find('a').get_text().strip()
        response = requests.get(link)
        encoding = cchardet.detect(response.content)['encoding']
        page = response.content.decode(encoding)
        soup_article = BeautifulSoup(page, 'lxml')
```
6) We extract the required data which are title, author, content, published date, and lastly, URL.
```
        author = soup_article.find('div', class_='ssrcss-68pt20-Text-TextContributorName e8mq1e96').get_text().split("By ")[1]
        date = soup_article.find('time')['datetime']
        body = soup_article.find_all(
            'article', class_='ssrcss-pv1rh6-ArticleWrapper e1nh2i2l6')
        x = body[0].find_all('p')

        # Unifying the paragraphs
        list_paragraphs = []
        for p in np.arange(0, len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
            content = " ".join(list_paragraphs)

        # Merged all the article details into one
        parsed_article = {'Title': title, 'Author': author,
                            'Published Date': date, 'Content': content, 'URL': link}

        parsed_articles.append(parsed_article)
```
7) If there are any errors in parsing and in extracting data, an error log is displayed.
```
    except:
        print("[ERROR] News article parsing error!")
```
8) The parsed articles will be returned as it will used for future processing which is the summary.
```
return parsed_articles
```