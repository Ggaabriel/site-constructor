import React from "react";
import { useAppSelector } from "src/app/hooks/useAppSelector";

const Profile: React.FC = () => {
  const id = useAppSelector((state) => state.user.user?.id);

  return (
    // <div className="pt-[4vh] pb-[20vh] ">
    //   <ul className="flex flex-col gap-[6vh]">
    //     <li className="flex justify-between items-center">
    //       <span className="text-20 font-bold  text-main">День рождения </span>
    //       <span className="text-16 text-main">20.01.2004</span>
    //     </li>
    //     <li className="flex justify-between items-center">
    //       <span className="text-20 font-bold  text-main">Номер телефона</span>
    //       <span className="text-16 text-main">+7 905 241 81 61</span>
    //     </li>
    //     <li className="flex justify-between items-center">
    //       <span className="text-20 font-bold  text-main">Соц. сети</span>
    //       {/* <span className="t1text-16t-20 text-main">Евгений</span> */}
    //     </li>
    //     <li className="flex justify-between items-center">
    //       <span className="text-20 font-bold  text-main">Биография</span>
    //       <p className="text-20 1text-16 text-main">Евгений</p>
    //     </li>
    //   </ul>
    // </div>
    <>{id}</>
  );
};

export default Profile;
