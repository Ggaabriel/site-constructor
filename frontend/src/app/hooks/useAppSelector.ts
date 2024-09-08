import { useSelector } from "react-redux";
import { TypedUseSelectorHook } from "react-redux";
import type { RootState } from "../store";

/** **useAppSelector** - это redux хук useSelector со строгой типизацией */
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
