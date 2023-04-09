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
      .get(`http://127.0.0.1:8000/api/articles/?page=${page}`)
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
