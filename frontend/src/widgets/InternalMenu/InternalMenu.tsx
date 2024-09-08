import React, { useRef } from "react";
import { NavLink } from "react-router-dom";
import Underline from "src/shared/Underline/Underline";
import { IInternalMenu } from "./interalMenuModel";

const InternalMenu: React.FC<IInternalMenu> = ({ MenuInfo }) => {
  const ref = useRef(null);
  return (
    <div>
      <ul ref={ref} className="flex justify-center gap-[16px]">
        {MenuInfo.map(({ path, title }, i) => (
          <li key={i} className="text-white">
            <NavLink className={`font-semibold text-14`} to={path} end>
              {title}
            </NavLink>
          </li>
        ))}
      </ul>
      <Underline fatherBlock={ref} />
    </div>
  );
};

export { InternalMenu };
