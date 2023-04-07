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
