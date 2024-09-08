export interface IMenu {
  link?: string;
  Image?: React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
  handleClick?: (n: unknown) => void;
}

export interface IMenuItem {
  menuItem: IMenu[];
}
