import { FC } from "react";
import { IInputDefaultProps } from "./InputDefaultModel";

const InputDefault: FC<IInputDefaultProps> = ({
  name,
  type,
  maxLength,
  placeholder,
  handleChange,
  disabled,
  valueInp,
  handelFocus,
  handelBlur,
  defaultValue,
  className,
}) => {
  const change = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleChange(e.target.value);
  };
  return (
    <input
      disabled={disabled}
      name={name}
      type={type}
      maxLength={maxLength}
      className={`text-[16px] focus:bg-white focus:text-mainBlack outline-none text-main border-[1px] not-italic font-semibold capitalize tracking-[-1.2px] bg-main/0 rounded-[10px] h-[50px] w-full indent-5 placeholder:text-main/50 focus:placeholder:text-mainBlack/50 ${className}`}
      placeholder={placeholder}
      value={"" || valueInp}
      onChange={change}
      onFocus={handelFocus}
      onBlur={handelBlur}
      defaultValue={defaultValue}
    />
  );
};
export { InputDefault };
