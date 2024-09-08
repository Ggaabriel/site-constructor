import React from "react";
import { Outlet } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";

import style from "./menu.module.css";
import { CustomLink } from "src/shared/CustomLink/CustomLink";
import { IMenuItem } from "./MenuModel";

const Menu: React.FC<IMenuItem> = ({ menuItem }) => {
  console.log("render");

  return (
    <>
      <Outlet />
      <AnimatePresence mode="wait">
        <motion.nav
          key={menuItem.toString()}
          initial={{
            opacity: 0,
          }}
          animate={{
            opacity: 1,
          }}
          exit={{
            opacity: 0,
          }}
          className={`fixed  py-[33px] px-[48px] bg-black/50 rounded-20 left-1/2 -translate-x-1/2 bottom-[20px] z-50 duration-200 ${style.menu}`}
        >
          <motion.ul
            key={menuItem.toString()}
            initial={{
              gap: 0,
              scale: 0,
            }}
            animate={{
              gap: "8vw",
              scale: 1,
            }}
            exit={{
              gap: 0,
              scale: 0,
            }}
            className="flex justify-center"
          >
            {menuItem.map(({ link, Image, handleClick }, i) => {
              return (
                <motion.li
                  whileTap={{ scale: 0.9 }}
                  key={i}
                  onClick={handleClick}
                >
                  <CustomLink to={link} Image={Image!} />
                </motion.li>
              );
            })}
          </motion.ul>
        </motion.nav>
      </AnimatePresence>
    </>
  );
};

export { Menu };
