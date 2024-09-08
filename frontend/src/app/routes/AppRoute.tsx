import React, { Suspense, useContext } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import {
  appRoutes,
  galleryRoutes,
  profileRoutes,
  projectRoutes,
} from "./routes";
import { Menu } from "src/widgets/Menu/Menu";
import { ProfileHeader } from "src/widgets/ProfileHeader/ProfileHeader";
import { GalleryHeader } from "src/widgets/GalleryHeader/GalleryHeader";
import { menuContext } from "../context";
import Loader from "src/shared/Loader/Loader";

const AppRoute: React.FC = () => {
  const { menuItems } = useContext(menuContext);
  return (
    <>
      <Suspense fallback={<Loader />}>
        <Routes>
          <Route path="/" element={<Navigate to={"/home"} />} />
          <Route element={<Menu menuItem={menuItems} />}>
            {appRoutes.map(({ Component, path }) => (
              <Route key={path} path={path} element={<Component />} />
            ))}
            <Route element={<ProfileHeader />}>
              {profileRoutes.map(({ Component, path }) => (
                <Route key={path} path={path} element={<Component />} />
              ))}
            </Route>
            <Route element={<GalleryHeader />}>
              {galleryRoutes.map(({ Component, path }) => (
                <Route key={path} path={path} element={<Component />} />
              ))}
            </Route>
            {projectRoutes.map(({ Component, path }) => (
              <Route key={path} path={path} element={<Component />} />
            ))}
          </Route>
        </Routes>
      </Suspense>
    </>
  );
};

export { AppRoute };
