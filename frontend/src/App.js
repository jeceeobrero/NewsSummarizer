import React, { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import axios from "axios";
import Home from "./components/Home";
import DetailNewsArticle from "./components/DetailNewsArticle";
import NotFound from "./components/NotFound";

const App = () => {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Home />}/>
          <Route path="/newsarticle" element={<DetailNewsArticle />}/>
          <Route path="*" element={<NotFound />}/> // Add this catch-all route at the bottom to render Not Found page
        </Routes>
      </div>
    </Router>
  );
}

export default App;