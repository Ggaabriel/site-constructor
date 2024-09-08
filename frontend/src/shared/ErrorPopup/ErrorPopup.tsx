import React from "react";
import { type IErrorPopup } from "./ErrorPopupModel";

const ErrorPopup: React.FC<IErrorPopup> = ({ errorMessage, handleClick }) => {
  return (
    <div className="fixed top-0 left-0 w-full h-full bg-black/50 z-50 flex justify-center items-center">
      <div className="p-4 max-w-[300px] w-full bg-red-500 text-white rounded-20 text-center">
        {errorMessage}
        <button
          onClick={handleClick}
          className="px-6 py-4 bg-red-800 rounded-20 mt-4 w-full"
        >
          ок
        </button>
      </div>
    </div>
  );
};

export { ErrorPopup };
