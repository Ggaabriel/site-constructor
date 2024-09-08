export interface INode {
  parent: string;
  id: string;
  type_id: "container" | "text" | "image";
  children: INode[];
  attrs: {
    [key: string]: string;
  };
}
interface IContainerAttrs {
  background: string;
  direction: string;
  [key: string]: string | undefined;
}

interface ITextAttrs {
  color: string;
  position: string;
  text: string;
  [key: string]: string | undefined;
}

interface IImageAttrs {
  src: string;
  alt: string;
  [key: string]: string | undefined;
}

export interface ITreeNode {
  id: string;
  type_id: "container" | "text" | "image";
  attrs: IContainerAttrs | ITextAttrs | IImageAttrs;
  children: ITreeNode[];
  holder: boolean;
}

export interface IPostNode {
  parent: string;
  template_id: string;
}
