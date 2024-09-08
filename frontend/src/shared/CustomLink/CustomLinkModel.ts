import { SVGProps } from "react";

export interface ICustomLink {
  Image: React.FC<SVGProps<SVGSVGElement>>;
  to?: string;
}
