import { createSlice } from "@reduxjs/toolkit";

interface IProject {
  parent: string;
  name: string;
}
interface IInitialState {
  projects: IProject[] | null;
  status: string;
}

const initialState: IInitialState = {
  projects: null,
  status: "ok",
};

export const projectsSlice = createSlice({
  name: "projects",
  initialState,
  reducers: {
    setProjects(state, action) {
      state.projects = action.payload;
    },
  },
});
export const { setProjects } = projectsSlice.actions;
export default projectsSlice.reducer;
