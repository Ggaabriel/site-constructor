import React from "react";
import { type IAddButton } from "./AddButtonModel";
import { motion } from "framer-motion";

const AddButton: React.FC<IAddButton> = ({ handleClick, className }) => {
  return (
    <motion.button
      onClick={handleClick}
      className={` w-full h-full text-4xl rounded-20 duration-200 p-2 ${className}`}
    >
      <div className="border-2 border-dashed border-black w-full h-full rounded-20 flex justify-center items-center">
        +
      </div>
    </motion.button>
  );
};

export { AddButton };
