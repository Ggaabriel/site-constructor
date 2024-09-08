import { createAsyncThunk } from "@reduxjs/toolkit";
import { axiosBase } from "src/app/http";

export const getUser = createAsyncThunk("getUser", async (id: string) => {
  return await axiosBase.get(`users/${id}`).then(({ data }) => data);
});

// import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
// import { baseURL } from 'src/app/http';
// interface IUser {
//     id: string;
//     login: string;
//   }
// export const userApi = createApi({
//   reducerPath: 'userApi',
//   tagTypes: ['User'],
//   baseQuery: fetchBaseQuery({ baseUrl: baseURL }),
//   endpoints: (builder) => ({
//     getUserById: builder.query<IUser, void>({
//       query: (userId) => `user/${userId}/`,
//       providesTags: (result) =>
//         result
//           ? [{ type: 'User', id: 'USER' }]
//           : [{ type: 'User', id: 'USER' }],
//     }),
//   }),
// });

// export const { useGetUserByIdQuery } = userApi;
