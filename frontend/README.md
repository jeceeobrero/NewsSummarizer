## FRONTEND 
# This is the frontend for the News Articles app which displays list of articles and its summaries. This uses ReactJS Framework due to its dynamic features and its helpful libraries.

## Features
1) Displays the list of articles including their title, author, published date, and a sneak peak of its summary in the Home Page sorted by the latest date.
2) Implemented clickable articles that open a detailed view, showing the full summary and a link to the original article.
3) It contains a search bar to filter articles by keywords from its title and summary, and its source.
4) It has pagination to limit the number of articles displayed per page.
5) It is a responsive application that can be accessed with a mobile phone, tab, and desktop.

# How the Page looks like
- First page displays the Home Page with the Home Component. This also renders the News Articles Component, SearchInput Component, Title Component, Badge Component, and 
- In News Articles Component, it displays the News Article Component.
- When you clicked the News Article Component, it will display the Detailed News Article Component.

# Components are 
1) DetailNewsArticle.js - display the clicked article among the articles displayed from the Home Page and it displays information such as title, author, published date, source, summary, and the source link.
```
import React from "react";
import { useLocation } from "react-router-dom";
import { Link } from "react-router-dom";
import Badge from "./Badge";

const DetailNewsArticle = () => {
  const location = useLocation();
  const data = location.state;
  const newsArticle = data ? data : "";

  return (
    <div className="mt-5 h-100 w-50 mx-auto">
      <Link to="/">Go back to Home</Link>
      <h1 className="news__title mt-5">{newsArticle.title}</h1>
      <Badge label={newsArticle.source} />
      <span className="ml-2 news__author">{newsArticle.author}</span>
      <p className="news__published">
        {newsArticle.published_date.substring(0, 10)}
      </p>
      <p className="news__desc text-justify">
        {newsArticle.summarized_content}
      </p>
      <a href={newsArticle.url} target="_blank">Go to its article link.</a>
    </div>
  );
};

export default DetailNewsArticle;
```

2) Home.js - displays the list of articles sorted by latest date with information such as title, author, published date, source, and a sneak peak of its summary. It has pagination where it displays six articles at most. We don't need to use virtualization of data since we already have implemented pagination in the server-side and it only renders 6 pages at most. Virtualization of data is useful whenever large list of data is to be rendered to avoid extensive usage of resources.

When we access the Home Page, it will immediately fire the GET news articles API with the page set initially as one. Whenever we go to another page number, the GET API is called and renders new articles on the page. It also checks if total page is not zero or empty so it won't display a blank page.
```
import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import { TransitionGroup, CSSTransition } from "react-transition-group";
import SearchInput from "./SearchInput";
import NewsArticles from "./NewsArticles";
import Heading from "./Heading";
import Pagination from "./Pagination";
import "../App.css";
import load from '../static/images/loading.gif'

const Home = () => {
  const [newsArticles, setNewsArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchValue, setSearchValue] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    // Call the API immediately
    fetchNewsArticles(currentPage);
  }, [currentPage]);

  // Create a GET call with pagination. This is useful whenever there are too many pages.
  // Instead of loading it all at once, just call the page needed to render. 
  const fetchNewsArticles = async (page) => {
    setError(null);
    setLoading(true);
    const res = await axios
      .get(`https://nlpnewsummarizer.azurewebsites.net/api/articles/?page=${page}`)
      .then((response) => {
        console.log(response);
        setTotalPages(response.data.total_pages);
        setNewsArticles(response.data.news_articles);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  };

  // Change page and use the useCallback hook to memoize the function and avoid unnecessary re-renders.
  const paginate = useCallback((pageNumber) => {
    if (pageNumber >= 1 && pageNumber <= totalPages) {
      setCurrentPage(pageNumber);
    }
  }, [totalPages]);

  return (
    <div className="container mt-5">
      <Heading />
      <SearchInput setSearchValue={setSearchValue} />
      <TransitionGroup>
        {loading ? (
          <h5>Loading <img src={load} className="loading__gif" alt="loading" /></h5>
        ) : error ? (
          <p>{error}</p>
        ) : (
          <>
            <CSSTransition key={currentPage} timeout={100} classNames="fade">
              <NewsArticles
                articles={newsArticles}
                searchVal={searchValue}
                loading={loading}
              />
            </CSSTransition>
            {totalPages > 1 && (
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                paginate={paginate}
              />
            )}
          </>
        )}
      </TransitionGroup>
    </div>
  );
};

export default Home;
```
3) NewsArticles.js - this serves as the container of the NewsArticle.js and contains the logic for filtering the news articles according to the keywords and their source. It displays six articles at most. We don't need to use virtualization of data since we already have implemented pagination in the server-side and it only renders 6 pages at most. Virtualization of data is useful whenever large list of data is to be rendered to avoid extensive usage of resources.
```
import React, { useState, useEffect } from "react";
import NewsArticle from "./NewsArticle";

const NewsArticles = ({ articles = [], searchVal = '', loading = false }) => {
  if (loading) {
    return <h2>Loading...</h2>;
  }
  
  return (
    <div className="all__news">
      {articles.filter((article)=> {
        return (
            searchVal === "" ||
            article.title.toLowerCase().includes(searchVal.toLowerCase()) ||
            article.source.toLowerCase().includes(searchVal.toLowerCase()) ||
            article.summarized_content.toLowerCase().includes(searchVal.toLowerCase())
        );
      }).map((article) => {
        return(
          <NewsArticle newsArticle={article} loading={loading}/>
        );
      })}
    </div>
  );
};

export default NewsArticles;
```
4) NewsArticle.js - this serves as the news article component that is displayed in the home page. This contains the article's title, author, published date, source, and a sneak peak of its summary.
```
import React from "react";
import { Link } from "react-router-dom";
import Badge from "./Badge";
const NewsArticle = ({ newsArticle, loading }) => {
  if (loading) {
    return <h2>Loading...</h2>;
  }

  return (
    <Link to="/newsarticle" state={newsArticle} className="news__article">
      <div className="news">
        <h1 className="news__title ">{newsArticle.title}</h1>
        <Badge label={newsArticle.source} />
        <span className="news__author">{newsArticle.author}</span>
        <p className="news__published">
          {newsArticle.published_date.substring(0, 10)}
        </p>
        <div className="container__news__desc">
          <p className="news__desc">{newsArticle.summarized_content}</p>
        </div>
        <button className="btn btn-link mt-3 text-primary p-0">
          Read More
        </button>
      </div>
    </Link>
  );
};

export default NewsArticle;
```
5) Pagination.js - serves as the display of the pagination ui.
```
import React from 'react';

const Pagination = ({ currentPage, totalPages, paginate }) => {
  const pageNumbers = [...Array(totalPages).keys()].map(i => i + 1);

  return (
    <nav>
     <ul className='pagination my-5 mx-auto float-right'>
        {pageNumbers.map(number => (
          <li key={number} className={`page-item${number === currentPage ? ' active' : ''}`}>
            <a onClick={() => paginate(number)} href={`#`} className='page-link'>
              {number}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Pagination;
```
6) Heading.js - contains the heading of the app
```
import React from "react";
import Badge from "./Badge";

const Heading = () => {
  return (
    <h2 className="col text-dark mb-3 p-0">
      Get Latest News Articles from {" "}
      <Badge label="BBC" />
      <Badge label="Daily Mail" />
      <Badge label="The Guardian" />
    </h2>
  );
};

export default Heading;
```
7) Badge.js - contains the display of badge or source of the article. This displays specific color for each news source.
```
import React from "react";

const Badge = ({ label }) => {
  const getBadgeColor = (source) => {
    let color;
    if (source === "BBC") {
      color = "badge-primary";
    } else if (source === "Daily Mail") {
      color = "badge-success";
    } else if (source === "The Guardian") {
      color = "badge-warning";
    }

    return color;
  };
  return <span className={"badge mx-1 badge " + getBadgeColor(label)}>{label}</span>;
};

export default Badge;
```
8) SearchInput.js - contains the search input which can filter news articles by title, keywords, and source.
```
import React from "react";

const SearchInput = ({ setSearchValue }) => {
  return (
    <div className="form-group mt-5">
      <input
        className="form-control"
        id="inputdefault"
        type="text"
        placeholder="Search for an article by title, keyword, or news source"
        onChange={(e) => setSearchValue(e.target.value.toLowerCase())}
      />
    </div>
  );
};

export default SearchInput;
```
9) NotFound.js - template for paths that are not specified in routes
```
import React from 'react';

const NotFound = () => {
  return (
    <div className="container mt-5">
      <h1>Page Not Found</h1>
      <p>The page you are looking for does not exist.</p>
    </div>
  );
};

export default NotFound;
```