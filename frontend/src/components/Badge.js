import React from "react";

const Badge = ({ label }) => {
  const getBadgeColor = (source) => {
    let color;
    if (source === "BBC") {
      color = "badge-primary";
    } else if (source === "Daily Mail") {
      color = "badge-success";
    } else if (source === "The Guardian") {
      color = "badge-warning";
    }

    return color;
  };
  return <span className={"badge mx-1 badge " + getBadgeColor(label)}>{label}</span>;
};

export default Badge;
