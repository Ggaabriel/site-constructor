import { useDispatch } from "react-redux";
import type { AppDispatch } from "../store";
/** **useAppDispatch** - это redux хук useDispatch со строгой типизацией */
export const useAppDispatch = () => useDispatch<AppDispatch>();
