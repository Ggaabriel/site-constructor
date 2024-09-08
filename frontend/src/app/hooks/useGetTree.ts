import { useEffect, useState } from "react";
import { useFetchQuery } from "./useFetchQuery";
import { IProject } from "../types/project.types";
import { useLazyGetTemplateQuery } from "../store/slice/UserPgaeSlice/UserPageApi";

const useGetTree = <T>(projectId: string) => {
  const [getTemplate] = useLazyGetTemplateQuery();
  const { data: project, isSuccess: isProjectSuccess } =
    useFetchQuery<IProject>({
      index: ["getProject", projectId],
      url: `projects/${projectId}`,
      isModalLoading: false,
    });

  const { data: tree, isSuccess: isTreeSuccess } = useFetchQuery<T>({
    index: "getTreeNodes",
    url: `/nodes/tree/${project?.core_node_id}`,
    isModalLoading: false,
    enabled: isProjectSuccess,
  });

  const { data: templateIds, isSuccess: isTemplatesSuccess } = useFetchQuery<
    string[]
  >({
    index: "getAllTemplates",
    url: `templates/`,
    isModalLoading: false,
    enabled: isTreeSuccess,
  });

  const [templates, setTemplates] = useState<any[]>([]);
  const [isTemplatesLoaded, setIsTemplatesLoaded] = useState(false);

  useEffect(() => {
    if (isTemplatesSuccess && templateIds) {
      const fetchTemplates = async () => {
        const templatePromises = templateIds.map((id) =>
          getTemplate(id).unwrap(),
        );
        const templatesData = await Promise.all(templatePromises);
        setTemplates(templatesData);
        setIsTemplatesLoaded(true);
      };
      fetchTemplates();
    }
  }, [isTemplatesSuccess, templateIds, getTemplate]);

  const getIdByType = (type: string) => {
    for (const elem of templates) {
      if (elem.tree.type_id === type) {
        return elem.id;
      }
    }
    return "id not found";
  };

  return { tree, isTreeSuccess, templates, isTemplatesLoaded, getIdByType };
};

export default useGetTree;
