import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";

type Props = {
  fatherBlock:
    | React.MutableRefObject<HTMLUListElement>
    | React.MutableRefObject<null>;
};
const Underline: React.FC<Props> = ({ fatherBlock }) => {
  const location = useLocation();
  const [underlineStyle, setUnderlineStyle] = useState({});
  const [activeMenuItem, setActiveMenuItem] = useState<HTMLLinkElement>();
  useEffect(() => {
    if (fatherBlock.current !== null) {
      const menuItems: NodeListOf<HTMLLinkElement> =
        fatherBlock.current.querySelectorAll("li a");
      const activeMenuItem = Array.from(menuItems).find(
        (item) => location.pathname === item.getAttribute("href"),
      );
      setActiveMenuItem(activeMenuItem);
      moveUnderline(activeMenuItem);
    }
    function moveUnderline(activeMenuItem: HTMLLinkElement | undefined) {
      if (activeMenuItem) {
        const { offsetLeft, offsetWidth } = activeMenuItem;
        setUnderlineStyle({
          left: `${offsetLeft}px`,
          width: `${offsetWidth}px`,
        });
      }
    }

    window.addEventListener("resize", () => moveUnderline(activeMenuItem));
    return () =>
      window.removeEventListener("resize", () => moveUnderline(activeMenuItem));
  }, [location, fatherBlock, activeMenuItem]);

  return (
    <div
      className=" absolute h-[2px] bg-white transition-all duration-300"
      style={underlineStyle}
    ></div>
  );
};

export default Underline;
