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