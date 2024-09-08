import React from "react";
import { Outlet } from "react-router-dom";
import { InternalMenu } from "../InternalMenu/InternalMenu";
import { RoutesList } from "src/app/types/routes/types";

const GalleryHeader: React.FC = () => {
  const MenuInfo = [
    {
      path: RoutesList.Gallery,
      title: "Популярные",
    },
    {
      path: RoutesList.GalleryFollowing,
      title: "Избранные",
    },
    {
      path: RoutesList.GalleryNew,
      title: "Новые",
    },
    {
      path: RoutesList.GalleryPersonal,
      title: "Мои",
    },
  ];
  return (
    <>
      <div className="container pt-[4vh] min-h-[100dvh]">
        <InternalMenu MenuInfo={MenuInfo} />
        <Outlet />
      </div>
    </>
  );
};

export { GalleryHeader };
