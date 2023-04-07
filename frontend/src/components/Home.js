import React, { useState, useEffect } from "react";
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
  const [newsArticlesPerPage] = useState(6);
  const [searchValue, setSearchValue] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    // Call the API immediately
    fetchNewsArticles();
  }, []);

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

  const updateLatestNewsArticles = async () => {
    setLoading(true);
    const res = await axios.post("https://nlpnewsummarizer.azurewebsites.net/api/articles/")
    .then((response) => {
      setLoading(false);
      fetchNewsArticles();
    })
    .catch((error) => {
      console.log(error); 
    })
  };

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
          <h5>Loading <img src={load} className="loading__gif" alt="loading" /></h5>
        ) : error ? (
          <p>{error}</p>
        ) : (
          <>
            <button className="btn btn-primary my-2" onClick={updateLatestNewsArticles}>Update Latest Articles</button>
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
