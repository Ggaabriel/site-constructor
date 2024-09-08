import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { ITreeNode } from "src/app/types/nodes";

const initialState: ITreeNode = {
  id: "0",
  children: [],
  type_id: "container",
  attrs: {
    direction: "flex-col",
    background: "#ffffff",
  },
  holder: true,
};

export const userPageSlice = createSlice({
  name: "projects",
  initialState,
  reducers: {
    setCoreNewChild(state, action) {
      state.children.push(action.payload);
    },
    setExistNewChild(state, action) {
      const { newChild, id } = action.payload;
      const existingItem = findIdInNestedObjects(state, id);
      if (existingItem) {
        existingItem.children = existingItem.children
          ? [...existingItem.children, newChild]
          : [newChild];
      }
    },
    // setPage(state, action: PayloadAction<ITreeNode>) {
    //   const { id } = action.payload;
    //   const existingItem = findIdInNestedObjects(state, id);

    //   if (!existingItem) {
    //     state.children.push(action.payload);
    //   } else {
    //     const newChild: ITreeNode = {
    //       id,
    //       children: [],
    //     };
    //     existingItem.children = existingItem.children
    //       ? [...existingItem.children, newChild]
    //       : [newChild];
    //   }
    // },
    setChildrens(
      state,
      action: PayloadAction<{ id: string; children: Array<string> }>,
    ) {
      const node = findIdInNestedObjects(state, action.payload.id);
      if (!node) {
        console.error(
          `Can't update children: node with ID ${action.payload.id} not found`,
        );
        return;
      }
      const tmp = [...node.children];
      node.children = new Array<ITreeNode>();
      for (const child_id of action.payload.children) {
        const new_node = tmp.find((value) => value.id === child_id);
        if (!new_node) {
          console.error(`Can't find node with ID ${child_id}`);
          return;
        }
        node.children.push(new_node);
      }
    },
    setTree(_, action: PayloadAction<ITreeNode>) {
      return action.payload;
    },
    deleteNode(state, action: PayloadAction<string>) {
      const targetId = action.payload;
      const parent = findParentNode(state, targetId);

      if (parent) {
        parent.children = parent.children.filter(
          (child) => child.id !== targetId,
        );
      } else {
        state.children = state.children.filter(
          (child) => child.id !== targetId,
        );
      }
    },
    updateNode(
      state,
      action: PayloadAction<{ id: string; updatedValues: Partial<ITreeNode> }>,
    ) {
      const { id, updatedValues } = action.payload;
      const node = findIdInNestedObjects(state, id);
      if (node) {
        Object.assign(node, updatedValues);
      }
    },
  },
});

const findIdInNestedObjects = (
  obj: ITreeNode,
  targetId: string,
): ITreeNode | null => {
  const stack: ITreeNode[] = [obj];

  while (stack.length > 0) {
    const node = stack.pop();
    if (!node) continue;

    if (node.id === targetId) {
      return node;
    }

    stack.push(...node.children);
  }

  return null;
};

const findParentNode = (obj: ITreeNode, targetId: string): ITreeNode | null => {
  const stack: { node: ITreeNode; parent: ITreeNode | null }[] = [
    { node: obj, parent: null },
  ];

  while (stack.length > 0) {
    const { node, parent } = stack.pop()!;

    if (node.id === targetId) {
      return parent;
    }

    for (const child of node.children) {
      stack.push({ node: child, parent: node });
    }
  }

  return null;
};

export const {
  // setPage,
  setTree,
  setCoreNewChild,
  setExistNewChild,
  deleteNode,
  setChildrens,
  updateNode,
} = userPageSlice.actions;
export default userPageSlice.reducer;
