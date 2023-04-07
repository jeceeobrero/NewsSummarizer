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
