import React, { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import axios from "axios";
import Home from "./components/Home";
import DetailNewsArticle from "./components/DetailNewsArticle";
import NotFound from "./components/NotFound";

const App = () => {
  return (
    <h1>Hi</h1>
    // <Router>
    //   <div>
    //     <Routes>
    //       <Route path="/" element={<Home />} />
    //       <Route path="/newsarticle" element={<DetailNewsArticle />} />
    //       <Route path="*" component={NotFound} />
    //     </Routes>
    //   </div>
    // </Router>
  );
}

export default App;