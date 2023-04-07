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
