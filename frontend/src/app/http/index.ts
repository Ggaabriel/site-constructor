import axios from "axios";
console.log(import.meta.env.VITE_API_URL);

/** axiosBase - это интерцептор для запросов на сервер */
export const axiosBase = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}/api/v1/`,
  headers: {
    "user-init-data": 'user={"id":"0"}',
  },
});
