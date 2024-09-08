import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface IInitialState {
  id: string;
  children: IInitialState[];
}

const initialState: IInitialState = {
  id: "0",
  children: [],
};

export const userPageSlice = createSlice({
  name: "projects",
  initialState,
  reducers: {
    setCoreNewChild(state, action: PayloadAction<IInitialState>) {
      state.children.push(action.payload);
    },
    setExistNewChild(state, action) {
      const { newChild, id } = action.payload;
      const existingItem = findIdInNestedObjects(state, id);
      existingItem!.children = existingItem!.children
        ? [...existingItem!.children, newChild]
        : [newChild];
    },
    setPage(state, action: PayloadAction<IInitialState>) {
      const { id } = action.payload;
      const existingItem = findIdInNestedObjects(state, id);

      if (!existingItem) {
        state.children.push(action.payload);
      } else {
        const newChild: IInitialState = {
          id,
          children: [],
        };
        existingItem.children = existingItem.children
          ? [...existingItem.children, newChild]
          : [newChild];
      }
    },
    setTree(_, action: PayloadAction<IInitialState>) {
      return action.payload;
    },
  },
});

const findIdInNestedObjects = (
  obj: IInitialState,
  targetId: string,
): IInitialState | null => {
  if (obj.id === targetId) {
    return obj;
  }
  for (const item of obj.children) {
    const result = findIdInNestedObjects(item, targetId);
    if (result) {
      return result;
    }
  }
  return null;
};

export const { setPage, setTree, setCoreNewChild, setExistNewChild } =
  userPageSlice.actions;
export default userPageSlice.reducer;
