import { useMutation, useQuery } from "react-query";
import { axiosBase } from "../http";
import { IProject } from "../types/project.types";
import { IPostNode, ITreeNode } from "../types/nodes";
/**
    Получение дерево "нод". 
    ****
    id* - id проекта. Он нужен для того, что бы получить id корневой "ноды".
*/
export const useGetTreeNode = (id: string) => {
  const { data: project } = useQuery({
    queryKey: "getProgect",
    queryFn: () =>
      axiosBase.get<IProject>(`projects/${id}`).then(({ data }) => data),
  });
  return useQuery({
    queryKey: "getTreeNodes",
    queryFn: () =>
      axiosBase
        .get<ITreeNode>(`nodes/tree/${project?.core_node_id}`)
        .then(({ data }) => data),
    enabled: !!project,
  });
};

export const usePostNode = () => {
  return useMutation({
    mutationKey: "postNode",
    mutationFn: (body: IPostNode) =>
      axiosBase.post<ITreeNode>(`nodes/`, body).then(({ data }) => data),
  });
};
