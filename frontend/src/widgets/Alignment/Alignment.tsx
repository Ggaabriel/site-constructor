import AlignCenter from "src/app/assets/icons/alignCenter.svg";
import AlignLeft from "src/app/assets/icons/alignLeft.svg";
import AlignRight from "src/app/assets/icons/alignRight.svg";

const Alignment = ({
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
          className="w-[105px] h-full flex items-center justify-center"
          onClick={() => {
            setAlign("text-left");
          }}
        >
          <img src={AlignLeft} alt="" />
        </li>
        <li
          className="w-[105px] h-full flex items-center justify-center"
          onClick={() => {
            setAlign("text-center");
          }}
        >
          <img src={AlignCenter} alt="" />
        </li>
        <li
          className="w-[105px] h-full flex items-center justify-center"
          onClick={() => {
            setAlign("text-right");
          }}
        >
          <img src={AlignRight} alt="" />
        </li>
      </ul>
      <div
        className="w-[105px] opacity-50 h-full bg-black absolute top-0 duration-200 "
        style={{
          left:
            align === "text-left"
              ? "0%"
              : align === "text-center"
                ? "50%"
                : align === "text-right"
                  ? "100%"
                  : "",
          transform:
            align === "text-left"
              ? "translateX(0%)"
              : align === "text-center"
                ? "translateX(-50%)"
                : align === "text-right"
                  ? "translateX(-100%)"
                  : "",
        }}
      ></div>
    </div>
  );
};

export default Alignment;
