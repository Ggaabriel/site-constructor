import React from "react";

const SkeletonProjectCard: React.FC = () => {
  return (
    <div className="bg-main/50 rounded-20 text-center p-[20px] flex flex-col justify-between min-h-[60dvh] animate-pulse"></div>
  );
};

export { SkeletonProjectCard };
