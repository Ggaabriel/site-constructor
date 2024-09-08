import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

import { IMenu } from "src/widgets/Menu/MenuModel";
import { menuItem } from "../routes/menuListItem";
import { menuContext } from "../context";

const MenuProvider = ({ children }: { children: React.ReactNode }) => {
  const [menuItems, setMenuItems] = useState<IMenu[]>(menuItem);
  const location = useLocation();
  useEffect(() => {
    if (location.pathname === "/" || location.pathname === "/home") {
      setMenuItems(menuItem);
    }
  }, [location]);

  return (
    <menuContext.Provider value={{ menuItems, setMenuItems }}>
      {children}
    </menuContext.Provider>
  );
};

export { MenuProvider };
