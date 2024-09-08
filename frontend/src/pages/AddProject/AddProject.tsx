import React, { useState } from "react";
import { InputDefault } from "src/shared/InputDefault/InputDefault";
import Back from "src/app/assets/icons/back.svg?react";
import Save from "src/app/assets/icons/save.svg?react";
import { useNavigate } from "react-router-dom";
import { useChangeMenu } from "src/app/hooks/useChangeMenu";
import { useFetchMutation } from "src/app/hooks/useFetchMutation";
import { IProject } from "src/app/types/project.types";

const AddProject: React.FC = () => {
  const [projectName, setProjectName] = useState<string>("");
  const navigate = useNavigate();
  const { mutate } = useFetchMutation<IProject>({
    index: "addProject",
    onSuccess: () => navigate(-1),
    body: { name: projectName },
    refetchKey: "getProjectsByUserId",
  });
  const menuItem = [
    {
      handleClick: () => navigate(-1),
      Image: Back,
    },
    {
      handleClick: () =>
        mutate({
          method: "POST",
          url: "projects",
        }),
      Image: Save,
    },
  ];
  useChangeMenu(menuItem);

  return (
    <>
      <div
        style={{ background: "linear-gradient(#7942D1, #E74EEA)" }}
        className="container pt-[4vh] min-h-[100dvh] min-w-[100vw] m-auto z-10 fixed top-0"
      >
        <div className="w-full max-w-[430px] mx-auto h-[70dvh] rounded-20 flex flex-col items-center relative z-20 gap-[20px]">
          <h2 className="text-[practice20px] font-bold uppercase text-main">
            Создать новый сайт
          </h2>
          <InputDefault
            type="text"
            name="projectName"
            handleChange={setProjectName}
            valueInp={projectName}
            placeholder="Мой проект"
          />
        </div>
      </div>
    </>
  );
};

export default AddProject;
