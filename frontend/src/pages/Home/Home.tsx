import React from "react";
import { EffectCoverflow, Pagination } from "swiper/modules";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";

import { ProjectCard } from "src/entities/ProjectCard/ProjectCard";
import { SkeletonProjectCard } from "src/entities/ProjectCard/SkeletonProjectCard";
import { AddCard } from "./AddCard";
import { useFetchQuery } from "src/app/hooks/useFetchQuery";
import { IProject } from "src/app/types/project.types";

const Home: React.FC = () => {
  const {
    data: projects = [],
    isLoading,
    isRefetching,
  } = useFetchQuery<IProject[]>({
    url: `projects/by/user/${0}`,
    index: "getProjectsByUserId",
    isModalLoading: false,
  });

  return (
    <div className="pt-[4vh] min-h-[100dvh]">
      <h1 className="title">Мои проекты</h1>
      <Swiper
        effect={"coverflow"}
        grabCursor={true}
        centeredSlides={true}
        slidesPerView={1.2}
        coverflowEffect={{
          rotate: 50,
          stretch: 0,
          depth: 100,
          modifier: 1,
          slideShadows: false,
        }}
        modules={[EffectCoverflow, Pagination]}
        pagination={true}
        className="h-full pt-[4dvh]"
      >
        {isLoading || isRefetching
          ? [...Array(10)].map((_, i) => (
              <SwiperSlide key={i}>
                <SkeletonProjectCard />
              </SwiperSlide>
            ))
          : projects?.map(({ id, name }) => (
              <SwiperSlide key={id}>
                <ProjectCard title={name} id={id!} />
              </SwiperSlide>
            ))}
        {!isLoading && (
          <SwiperSlide>
            <AddCard />
          </SwiperSlide>
        )}
      </Swiper>
    </div>
  );
};

export default Home;
