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
