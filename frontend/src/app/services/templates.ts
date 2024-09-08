import { useQuery } from "react-query";
import { axiosBase } from "../http";
import { ITemplate } from "../types/template";

export const useGetTemplate = () => {
  const { data: templateIds } = useQuery({
    queryKey: "getTemplateIds",
    queryFn: async () => {
      return await axiosBase
        .get("templates")
        .then<string[]>(({ data }) => data);
    },
  });

  return useQuery({
    queryKey: "getTemplate",
    queryFn: async () => {
      if (!templateIds || templateIds.length === 0) {
        return [];
      }

      const templatePromises = templateIds.map(async (id) => {
        return await axiosBase
          .get<ITemplate>(`templates/${id}`)
          .then(({ data }) => data);
      });

      return Promise.all(templatePromises);
    },
    enabled: !!templateIds?.length,
  });
};
