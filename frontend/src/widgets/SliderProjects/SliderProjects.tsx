import React from "react";
import { ProjectCard } from "src/entities/ProjectCard/ProjectCard";
import picture from "../../assets/picture.svg";
import "swiper/css";
import "swiper/css/effect-cards";
import { Link } from "react-router-dom";
import { RoutesList } from "src/app/types/routes/types";

interface IProject {
  id: string;
  name: string;
}

interface ISliderProjects {
  projects: IProject[] | null;
}

const SliderProjects: React.FC<ISliderProjects> = ({ projects }) => {
  return (
    // <Swiper
    //   effect={"coverflow"}
    //   grabCursor={true}
    //   centeredSlides={true}
    //   slidesPerView={1.2}
    //   coverflowEffect={{
    //     rotate: 50,
    //     stretch: 0,
    //     depth: 100,
    //     modifier: 1,
    //     slideShadows: false,
    //   }}
    //   pagination={true}
    //   modules={[EffectCoverflow, Pagination]}
    //   className="h-full"
    // >
    //   {[...Array(3)].map((_, i) => (
    //     <SwiperSlide
    //       key={i}
    //       className="bg-main rounded-20 min-h-[60dvh] w-full"
    //     ></SwiperSlide>
    //   ))}
    //   <SwiperSlide className="min-h-[60dvh] border-3 border-main rounded-20  w-full flex justify-center items-center text-[20dvh] font-light text-main">
    //     +
    //   </SwiperSlide>
    // </Swiper>
    <div className="h-fit w-full py-[4vh] px-[10px] grid gap-[20px] grid-cols-2 pb-[140px]">
      {projects?.map((item, i) => (
        <Link key={i} to={`/project/${item.id}`}>
          <ProjectCard title="project" id={item.id} />
        </Link>
      ))}
      <div className="bg-project border-3 text-main border-main rounded-20 h-[280px] text-center p-[20px] flex flex-col items-center justify-between">
        <h2 className="text-[practice20px] font-bold uppercase">
          СОЗДАТЬ САЙТ
        </h2>
        <Link
          to={"/projects/add"}
          className="w-full max-w-[70px] aspect-square rounded-full bg-main text-6xl flex items-center justify-center font-thin text-addProject cursor-pointer"
        >
          +
        </Link>
        <h2 className="text-[practice20px] font-bold uppercase">
          ИЛИ ВЫБРАТЬ ИЗ ГАЛЕРЕИ
        </h2>
        <Link className="max-w-[70px] aspect-square" to={RoutesList.Gallery}>
          <img className=" " src={picture} alt="" />
        </Link>
      </div>
    </div>
  );
};

export { SliderProjects };
