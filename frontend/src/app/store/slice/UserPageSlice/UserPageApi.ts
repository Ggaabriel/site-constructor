import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

interface INewNode {
  parent: string;
  children: [] | string[];
}

export const nodesApi = createApi({
  reducerPath: "nodesApi",
  baseQuery: fetchBaseQuery({
    baseUrl: "http://localhost/api/v1/",
    headers: {
      "user-init-data": 'user={"id":0}',
    },
  }),
  endpoints: (builder) => ({
    getNodes: builder.query({
      query: (nodeId) => `nodes/${nodeId}`,
    }),
    postNodes: builder.mutation({
      query: (body: INewNode) => ({
        url: "nodes/",
        method: "POST",
        body,
      }),
    }),
    patchNodes: builder.mutation({
      query: ({ nodeId, body }: { nodeId: string; body: INewNode }) => ({
        url: `nodes/${nodeId}`,
        method: "PATCH",
        body,
      }),
    }),
    deleteNodes: builder.mutation({
      query: (nodeId) => ({
        url: `nodes/${nodeId}`,
        method: "DELETE",
      }),
    }),
    getTreeNodes: builder.query({
      query: (nodeId) => `nodes/tree/${nodeId}`,
    }),
  }),
});

export const {
  useGetNodesQuery,
  usePostNodesMutation,
  usePatchNodesMutation,
  useDeleteNodesMutation,
  useGetTreeNodesQuery,
} = nodesApi;
