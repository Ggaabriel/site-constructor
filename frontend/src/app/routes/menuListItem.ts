import Gallery from "src/app/assets/icons/gallery.svg?react";
import Home from "src/app/assets/icons/home.svg?react";
import Profile from "src/app/assets/icons/profile.svg?react";
import Info from "src/app/assets/icons/info.svg?react";
import { RoutesList } from "src/app/types/routes/types";

export const menuItem = [
  {
    link: RoutesList.Home,
    Image: Home,
  },
  {
    link: RoutesList.Gallery,
    Image: Gallery,
  },
  {
    link: RoutesList.Info,
    Image: Info,
  },
  {
    link: RoutesList.Profile,
    Image: Profile,
  },
];

export const menuItem2 = [
  {
    link: RoutesList.Home,
    Image: Home,
  },
  {
    link: RoutesList.Gallery,
    Image: Gallery,
  },
];
