import { ITreeNode } from "src/app/types/nodes";

const RenderNode: React.FC<ITreeNode> = (node) => {
  return (
    <div>
      <div className="">RenderNode</div>
      {node.children?.map((node) => <RenderNode key={node.id} {...node} />)}
    </div>
  );
};

export { RenderNode };
