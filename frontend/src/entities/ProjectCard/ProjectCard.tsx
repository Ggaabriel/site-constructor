import React from "react";
import Edit from "src/app/assets/icons/edit.svg?react";
import LinkIcon from "src/app/assets/icons/link.svg?react";
import { Link, useNavigate } from "react-router-dom";
import { type IProjectCard } from "./projectCardModel";

const ProjectCard: React.FC<IProjectCard> = ({ title, id }) => {
  const navigate = useNavigate();
  return (
    <Link
      to={`/project/${id}`}
      className="bg-main rounded-20 text-center p-[20px] flex flex-col justify-between min-h-[60dvh]"
    >
      <h2 className="text-[practice20px] font-bold">{title}</h2>
      <div className="flex justify-between">
        <div
          onClick={(e) => {
            e.preventDefault();
            navigate(`/project/${id}/edit`);
          }}
        >
          <Edit stroke="black" className="h-5 w-5" />
        </div>
        <div
          onClick={(e) => {
            e.preventDefault();
            window.location =
              `${import.meta.env.VITE_API_URL}:7000/0/${id}/` as Location &
                string;
          }}
        >
          <LinkIcon fill="black" />
        </div>
      </div>
    </Link>
  );
};

export { ProjectCard };
