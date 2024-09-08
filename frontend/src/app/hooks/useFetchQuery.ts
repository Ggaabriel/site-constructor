import { useQuery } from "react-query";
import { axiosBase } from "../http";
import { useContext } from "react";
import { responseContext } from "../context";
import { IError, IFetchQuery } from "../types/fetch.types";

/** useFetchQuery - это кастомный хук, для  GET запросов.
 *
 * **index** - это параметр по которому можно повторить этот запрос (refetch).
 *
 * **onSuccess** - это callback фугкция, которая срабатывает только, если запрос прошел успешно
 *
 * **isModalLoading** - это параметр, который отвечает за отображение стандартного экрана загрузки или нет
 */
export const useFetchQuery = <AxiosFetch>({
  index,
  url,
  onSuccess,
  isModalLoading = true,
  enabled = true,
}: IFetchQuery) => {
  const { setResponse } = useContext(responseContext);
  return useQuery({
    queryKey: index,
    queryFn: async () => {
      isModalLoading && setResponse({ isLoading: true });
      return await axiosBase.get<AxiosFetch>(url).then(({ data }) => data);
    },
    onSuccess: () => {
      isModalLoading && setResponse({ isLoading: false });
      onSuccess && onSuccess();
    },
    onError: ({ response }: IError) => {
      setResponse({ errorMessage: response.data.detail });
    },
    enabled,
  });
};
