import React from "react";
import { Link, useMatch } from "react-router-dom";
import { type ICustomLink } from "./CustomLinkModel";

const CustomLink: React.FC<ICustomLink> = ({ Image, to }) => {
  const match = useMatch({ path: to ? to : "/", end: false });

  return (
    <>
      {to ? (
        <Link to={to}>
          <Image stroke={match ? "#FF78E9" : "#FFFFFF"} />
        </Link>
      ) : (
        <Image style={{ cursor: "pointer" }} stroke={"#FFFFFF"} />
      )}
    </>
  );
};

export { CustomLink };
