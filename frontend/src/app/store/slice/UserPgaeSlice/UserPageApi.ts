import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

interface INewNode {
  parent: string;
  template_id: string;
}
interface ITemplate {}
export const nodesApi = createApi({
  reducerPath: "nodesApi",
  baseQuery: fetchBaseQuery({
    baseUrl: `${import.meta.env.VITE_API_URL}/api/v1/`,
    headers: {
      "user-init-data": 'user={"id":"0"}',
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
      query: ({
        nodeId,
        body,
      }: {
        nodeId: string;
        body: { parent: string; position: number };
      }) => ({
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
    postTemplate: builder.mutation({
      query: (body: ITemplate) => ({
        url: "templates/",
        method: "POST",
        body,
      }),
    }),
    patchAttr: builder.mutation({
      query: (body) => {
        // Encode the attribute_value to ensure the # character is handled correctly
        const encodedValue = encodeURIComponent(body.attribute_value);
        return {
          url: `attrs/?node_id=${body.node_id}&attribute_name=${body.attribute_name}&attribute_value=${encodedValue}`,
          method: "PATCH",
        };
      },
    }),
    getTemplate: builder.query({
      query: (template_id: string) => ({
        url: `templates/${template_id}`,
      }),
    }),
    postPage: builder.mutation({
      query: (body) => ({
        url: `pages/${body.projectId}`,
        method: "POST",
      }),
    }),
  }),
});

export const {
  useGetNodesQuery,
  useLazyGetNodesQuery,
  usePostNodesMutation,
  usePatchNodesMutation,
  useDeleteNodesMutation,
  useGetTreeNodesQuery,
  usePatchAttrMutation,
  useLazyGetTemplateQuery,
  usePostPageMutation,
} = nodesApi;
