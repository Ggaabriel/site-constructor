import React from "react";

export interface IInputDefaultProps {
  name: string;
  type: string;
  maxLength?: number;
  placeholder?: string;
  handleChange: (event: string) => void;
  disabled?: boolean;
  valueInp?: string;
  handelFocus?: (event: React.FocusEvent<HTMLInputElement>) => void;
  handelBlur?: (event: React.FocusEvent<HTMLInputElement>) => void;
  defaultValue?: string;
  className?: string;
}
