# NEWS SUMMARIZER

This application parses articles from news sources namely, BBC, Daily Mail, and The Guardian, summarizes these articles, and display their information such as title, author, published date, source, url, and its summary. 

## How to run locally
- Type the command in command line.
```
    pip install - r requirements.txt
```
- Navigate to frontend directory and install npm.
```
    npm install
```
- Run npm build.
```
    npm run build
```
- Go back to the base directory where there is manage.py and run this command.
```
    python manage.py runserver
```

## Frontend API
This is the frontend for the News Articles app which displays list of articles and its summaries. This uses ReactJS Framework due to its dynamic features and its helpful libraries.

# Features
1) Displays the list of articles including their title, author, published date, and a sneak peak of its summary in the Home Page sorted by the latest date.
2) Implemented clickable articles that open a detailed view, showing the full summary and a link to the original article.
3) It contains a search bar to filter articles by keywords from its title and summary, and its source.
4) It has pagination to limit the number of articles displayed per page.
5) It is a responsive application that can be accessed with a mobile phone, tab, and desktop.

# How the Page looks like
- First page displays the Home Page with the Home Component. This also renders the Title Component, Badge Component, and Pagination Component. 
- Inside the Home Component is the News Articles Component and the SearchInput Component.
- In News Articles Component, it displays the News Article Component.
- When you clicked the News Article Component, it will display the Detailed News Article Component.

# Components are 
1) DetailNewsArticle.js - display the clicked article among the articles displayed from the Home Page and it displays information such as title, author, published date, source, summary, and the source link.
2) Home.js - displays the list of articles sorted by latest date with information such as title, author, published date, source, and a sneak peak of its summary. It has pagination where it displays six articles at most.
3) NewsArticles.js - this serves as the container of the NewsArticle.js and contains the logic for filtering the news articles according to the keywords and their source. 
4) NewsArticle.js - this serves as the news article component that is displayed in the home page. This contains the article's title, author, published date, source, and a sneak peak of its summary.
5) Pagination.js - serves as the display of the pagination ui.
6) Heading.js - contains the heading of the app
7) Badge.js - contains the display of badge or source of the article. This displays specific color for each news source.
8) SearchInput.js - contains the search input which can filter news articles by title, keywords, and source.
9) NotFound.js - template for paths that are not specified in routes

# Limitations
1) It does have error handling from the parsing of news articles and the summarizing of the news articles, to the actual display of the news articles. 
It displays errors however, it sometimes give vague errors. This will be great addition in the future of the News Summarization App.
2) It needs optimization both in frontend and backend (NLP) as well to make the app more robust. 

## Backend API

This Backend API displays and parses+summarizes three reputable sources namely, BBC, The Guardian, and Daily Mail. It uses Beautiful Soup for web scraping, GPT-3 for Summarizing and an REST API. This Backend uses Postgresql as its database. It contains News Article model containing title, author, published date, source, summary, and the source link. 

# Files
1) API - this contains the REST API methods such as GET News Articles and POST News Articles.
2) Scraper - parses for news articles from various sources such as BBC, The Guardian, and Daily Mail. It uses Beautiful Soup and lxml as the parser.
3) Summarizer - summarizes and display the brief and precise content of the news article. It uses GPT-3, an autoregressive language model released in 2020 that uses deep learning to produce human-like text.

# Methods
1) GET all news articles sorted according to the latest dates.
2) POST all parsed and summarized articles. 
- Since it involves list of articles, it is best to use atomic transaction in saving news articles which is implemented in this app.
- It also implements caching which will avoid duplication of parsing and summarizing procedures.
- It logs errors when it encountered one.

