import React from "react";
import Badge from "./Badge";

const Heading = () => {
  return (
    <h2 className="col text-dark mb-3 p-0">
      Get Latest News Articles from {" "}
      <Badge label="BBC" />
      <Badge label="Daily Mail" />
      <Badge label="The Guardian" />
    </h2>
  );
};

export default Heading;
