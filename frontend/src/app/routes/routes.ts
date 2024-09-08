import { RoutesList } from "../types/routes/types";
import { lazy } from "react";

export const appRoutes = [
  {
    path: RoutesList.Home,
    Component: lazy(() => import("src/pages/Home/Home")),
  },
  {
    path: RoutesList.Info,
    Component: lazy(() => import("src/pages/Info/Info")),
  },
];

export const projectRoutes = [
  {
    path: RoutesList.ProjectAdd,
    Component: lazy(() => import("src/pages/AddProject/AddProject")),
  },
  {
    path: RoutesList.Project,
    Component: lazy(() => import("src/pages/UserPage/UserPage")),
  },
  {
    path: RoutesList.ProjectEdit,
    Component: lazy(() => import("src/pages/Edit/Edit")),
  },
];

export const profileRoutes = [
  {
    path: RoutesList.Profile,
    Component: lazy(() => import("src/pages/Profile/Profile")),
  },
  {
    path: "/profile/awards/",
    Component: lazy(() => import("src/pages/Awards/Awards")),
  },
  {
    path: "/profile/quests/",
    Component: lazy(() => import("src/pages/Quests/Quests")),
  },
  {
    path: "/profile/settings/",
    Component: lazy(() => import("src/pages/ProfileSettings/ProfileSettings")),
  },
];

export const galleryRoutes = [
  {
    path: RoutesList.Gallery,
    Component: lazy(() => import("src/pages/Gallery/Popular")),
  },
  {
    path: "/gallery/following/",
    Component: lazy(() => import("src/pages/Gallery/Following")),
  },
  {
    path: "/gallery/new/",
    Component: lazy(() => import("src/pages/Gallery/New")),
  },
  {
    path: "/gallery/personal/",
    Component: lazy(() => import("src/pages/Gallery/Personal")),
  },
];
