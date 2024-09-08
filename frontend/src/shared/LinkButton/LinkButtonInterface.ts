export interface ILinkButtonProps {
  title: string | undefined;
  buttonActive: boolean;
  handleClick?: () => void;
  type: "button" | "reset" | "submit" | undefined;
}
