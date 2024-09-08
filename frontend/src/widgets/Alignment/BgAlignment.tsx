import Position from "src/app/assets/icons/position.svg";
const BgAlignment = ({
  setAlign,
  align,
}: {
  setAlign: (value: string) => void;
  align: string;
}) => {
  return (
    <div className="w-[307px] h-[30px] bg-slate-100 mx-auto rounded-[10px] shadow-lg relative overflow-hidden">
      <ul className="flex w-full h-full justify-between items-center ">
        <li
          className="w-[153px] h-full flex items-center justify-center"
          onClick={() => {
            setAlign("flex-col");
          }}
        >
          <img className="rotate-90" src={Position} alt="" />
        </li>
        <li
          className="w-[154px] h-full flex items-center justify-center"
          onClick={() => {
            setAlign("flex-row");
          }}
        >
          <img src={Position} alt="" />
        </li>
      </ul>
      <div
        className="w-[154px] opacity-50 h-full bg-black absolute top-0 duration-200 "
        style={{
          left: align === "flex-col" ? "0%" : "100%",
          transform:
            align === "flex-col" ? "translateX(0%)" : "translateX(-100%)",
        }}
      ></div>
    </div>
  );
};

export default BgAlignment;
