import { FC } from "react";
import { ILinkButtonProps } from "./LinkButtonInterface";
const LinkButton: FC<ILinkButtonProps> = ({
  title,
  buttonActive,
  handleClick,
  type,
}) => {
  return (
    <button
      type={type}
      disabled={buttonActive}
      className={`transition  w-full active:scale-90  text-white mx-auto  py-[15px] rounded-[15px] bg-gradient-to-r whitespace-nowrap disabled:opacity-50 from-black to-[#545454]`}
      onClick={handleClick}
    >
      {title}
    </button>
  );
};

export { LinkButton };
