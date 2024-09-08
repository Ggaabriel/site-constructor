import React from "react";
import practiceLogo from "src/app/assets/practiceLogo.png";
import style from "./loader.module.css";
const Loader: React.FC = () => {
  return (
    <div className={style.bg}>
      <img className={style.loader} src={practiceLogo} alt="" />
    </div>
  );
};

export default Loader;
