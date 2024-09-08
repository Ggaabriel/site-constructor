import React from "react";
import { useGetTemplate } from "src/app/services/templates";

const Popular: React.FC = () => {
  const { data: templates } = useGetTemplate();
  const templatesWithoutBaseTemplate = templates?.slice(3);
  if (!templatesWithoutBaseTemplate) {
    return null;
  }

  return (
    <div className="container pt-[4vh]">
      {templatesWithoutBaseTemplate?.length === 0 && (
        <span className="text-2xl text-white font-bold block text-center">
          Тут ничего нет
        </span>
      )}
    </div>
  );
};

export default Popular;
