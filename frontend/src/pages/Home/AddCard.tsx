import { Link } from "react-router-dom";

const AddCard = () => {
  return (
    <Link
      to={"/projects/add"}
      className="min-h-[60dvh] w-full h-full flex flex-col justify-center items-center border-3 border-main rounded-20  p-[20px]"
    >
      <span className="text-[20dvh] font-light text-main">+</span>
    </Link>
  );
};

export { AddCard };
