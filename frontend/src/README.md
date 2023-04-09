# This serves as the client-side that contains files that are needed to display the frontend for the news article app.

## How the Page looks like
- First page displays the Home Page with the Home Component. This also renders the Heading Component, Badge Component, and Pagination Component. 
- Inside the Home Component is the News Articles Component and the SearchInput Component.
- In News Articles Component, it displays the News Article Component.
- When you clicked the News Article Component, it will display the Detailed News Article Component.

## Components are 
1) DetailNewsArticle.js - display the clicked article among the articles displayed from the Home Page and it displays information such as title, author, published date, source, summary, and the source link.
This is the code snippit for the DetailNewsArticle.js.
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

2) Home.js - displays the list of articles sorted by latest date with information such as title, author, published date, source, and a sneak peak of its summary. It has pagination where it displays six articles at most.
```
import React, { useState, useEffect } from "react";
import axios from "axios";
import { TransitionGroup, CSSTransition } from "react-transition-group";
import SearchInput from "./SearchInput";
import NewsArticles from "./NewsArticles";
import Heading from "./Heading";
import Pagination from "./Pagination";
import "../App.css";

const Home = () => {
  const [newsArticles, setNewsArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [newsArticlesPerPage] = useState(6);
  const [searchValue, setSearchValue] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchNewsArticles = async () => {
      setError(null);
      setLoading(true);
      const res = await axios
        .get("https://nlpnewsummarizer.azurewebsites.net/api/articles/")
        .then((response) => {
          setNewsArticles(response.data.news_articles);
          setLoading(false);
        })
        .catch((error) => {
          setError(error.message);
          setLoading(false);
        });
    };

    // Call the API immediately
    fetchNewsArticles();
  }, []);

  // Get current news articles based on index indexOfFirstNewsArticle and indexOfLastNewsArticle
  const indexOfLastNewsArticle = currentPage * newsArticlesPerPage;
  const indexOfFirstNewsArticle = indexOfLastNewsArticle - newsArticlesPerPage;

  // Total News Articles
  const totalNewsArticles = newsArticles.length;

  //  Store a subset of filteredNewsArticles to display on the current page.
  const currentNewsArticles = newsArticles.slice(
    indexOfFirstNewsArticle,
    indexOfLastNewsArticle
  );

  // Change page
  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  const pageNumbers = [];

  for (
    let i = 1;
    i <= Math.ceil(totalNewsArticles / newsArticlesPerPage);
    i++
  ) {
    pageNumbers.push(i);
  }

  return (
    <div className="container mt-5">
      <Heading />
      <SearchInput setSearchValue={setSearchValue} />
      <TransitionGroup>
        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p>{error}</p>
        ) : (
          <>
            <CSSTransition key={currentPage} timeout={500} classNames="fade">
              <NewsArticles
                articles={currentNewsArticles}
                searchVal={searchValue}
                loading={loading}
              />
            </CSSTransition>
            <Pagination
              newsArticlesPerPage={newsArticlesPerPage}
              totalNewsArticles={newsArticles.length}
              paginate={paginate}
            />
          </>
        )}
      </TransitionGroup>
    </div>
  );
};

export default Home;
```
3) NewsArticles.js - this serves as the container of the NewsArticle.js and contains the logic for filtering the news articles according to the keywords and their source. 
```
import React, { useState, useEffect } from "react";
import NewsArticle from "./NewsArticle";

const NewsArticles = ({ articles, searchVal, loading }) => {
  const newsArticles = articles ? articles : "";
  const searchValue = searchVal ? searchVal : ""; 

  if (loading) {
    return <h2>Loading...</h2>;
  }
  
  return (
    <div className="all__news">
      {newsArticles.filter((article)=> {
        if(searchValue == ""){
          return article;
        }
        else if(article.title.toLowerCase().includes(searchValue.toLowerCase())){
          return article;
        }
        else if(article.source.toLowerCase().includes(searchValue.toLowerCase())){
          return article;
        }
        else if(article.summarized_content.toLowerCase().includes(searchValue.toLowerCase())){
          return article;
        }
      }).map((article, key) => {
        return(
          <NewsArticle newsArticle={article} loading={loading}/>
        );
      })}
    </div>
  );
};

export default NewsArticles;
```
4) NewsArticle.js - this serves as the news article component that is displayed in the home page. This contains the article's title, author, published date, source, and a sneak peak of its summary
```
import React from "react";
import { Link } from "react-router-dom";
import Badge from "./Badge";
const NewsArticle = ({ newsArticle, loading }) => {
  if (loading) {
    return <h2>Loading...</h2>;
  }

  return (
    <Link to="/newsarticle" state={newsArticle}>
      <div className="news" href="#">
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

const Pagination = ({ newsArticlesPerPage, totalNewsArticles, paginate }) => {
  const pageNumbers = [];

  for (let i = 1; i <= Math.ceil(totalNewsArticles / newsArticlesPerPage); i++) {
    pageNumbers.push(i);
  }

  return (
    <nav>
      <ul className='pagination my-5 mx-auto float-right'>
        {pageNumbers.map(number => (
          <li key={number} className='page-item'>
            <a onClick={() => paginate(number)} href={"#" + number} className='page-link'>
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
    <h2 className="col text-primary mb-5 p-0">
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
    <div className="form-group mb-5">
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
