import React from "react";
import { Link, Outlet } from "react-router-dom";
import { InternalMenu } from "../InternalMenu/InternalMenu";
import Settings from "src/app/assets/icons/settings.svg?react";
import { RoutesList } from "src/app/types/routes/types";

const ProfileHeader: React.FC = () => {
  const MenuInfo = [
    {
      path: RoutesList.Profile,
      title: "Профиль",
    },
    {
      path: RoutesList.ProfileSettings,
      title: "Награды",
    },
    {
      path: RoutesList.ProfileQuests,
      title: "Испытания",
    },
  ];
  return (
    <>
      <div className="container pt-[4vh] min-h-[100dvh] transition-[height]">
        <div className="flex flex-col items-center">
          <div className="h-[25vh] aspect-square bg-white/50 rounded-20 relative">
            <Link
              to={"profile/settings"}
              className="absolute -top-[10px] -right-[10px]"
            >
              <Settings stroke={"white"} />
            </Link>
          </div>
          <span className="title pt-[10px]">Eugene</span>
          <span className="text-white">студент</span>
        </div>
        <InternalMenu MenuInfo={MenuInfo} />
        <Outlet />
      </div>
    </>
  );
};

export { ProfileHeader };
