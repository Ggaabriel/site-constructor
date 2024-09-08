export interface ITemplate {
  id: string;
  tree: {
    id: string;
    type_id: "image" | "text" | "container";
    attrs: {
      [key: string]: string;
    };
    children: ITemplate[];
  };
}
