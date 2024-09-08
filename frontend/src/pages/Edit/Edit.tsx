import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

import Back from "src/app/assets/icons/back.svg?react";
import Save from "src/app/assets/icons/save.svg?react";
import { InputDefault } from "src/shared/InputDefault/InputDefault";
import { useChangeMenu } from "src/app/hooks/useChangeMenu";
import { useFetchMutation } from "src/app/hooks/useFetchMutation";
import { IProject } from "src/app/types/project.types";
import { useFetchQuery } from "src/app/hooks/useFetchQuery";
const Edit: React.FC = () => {
  const navigate = useNavigate();
  const [projectName, setProjectName] = useState<string>("");
  const { projectId } = useParams();
  const { mutate } = useFetchMutation({
    index: "editProfect",
    onSuccess: () => navigate(-1),
    body: { name: projectName },
    refetchKey: "getProjectsByUserId",
  });
  const { data: project } = useFetchQuery<IProject>({
    url: `projects/${projectId}`,
    index: "getProjectById",
  });
  useEffect(() => {
    if (project) {
      setProjectName(project.name);
    }
  }, [project]);

  const menuItem = [
    {
      handleClick: () => navigate(-1),
      Image: Back,
    },
    {
      handleClick: () =>
        mutate({
          url: `projects/${projectId}`,
          method: "PATCH",
        }),
      Image: Save,
    },
  ];
  useChangeMenu(menuItem);

  return (
    <div className="container pt-[4vh] min-h-[100dvh] transition-[height]">
      <div className="w-full h-[70dvh] rounded-20 flex flex-col items-center relative z-20 gap-[20px]">
        <span className="text-[practice20px] font-bold uppercase text-main">
          Редактировать сайт.
        </span>
        <InputDefault
          type="text"
          name="projectName"
          handleChange={setProjectName}
          valueInp={projectName}
          placeholder="Мой проект"
        />
        <button
          onClick={() =>
            mutate({
              url: `projects/${projectId}`,
              method: "DELETE",
            })
          }
          className="text-[20px] font-bold uppercase text-red-600"
        >
          Удалить сайт
        </button>
      </div>
    </div>
  );
};

export default Edit;
