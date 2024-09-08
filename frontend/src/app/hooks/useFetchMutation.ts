import { useMutation, useQueryClient } from "react-query";
import { IError, IFetchMutatuion } from "../types/fetch.types";
import { responseContext } from "../context";
import { useContext } from "react";
import { axiosBase } from "../http";

/** useFetchMutation - это кастомный хук, для всех запросов, кроме GET.
 *
 * **index** - это параметр по которому можно повторить этот запрос (refetch).
 *
 * **onSuccess** - это callback фугкция, которая срабатывает только, если запрос прошел успешно.
 *
 * **isModalLoading** - это параметр, который отвечает за отображение стандартного экрана загрузки или нет.
 *
 * **refetchKey** - это ключ (index) по которому будет проводится инвалидация кеша и обновление данных.
 *
 * Возвращаемые значения:
 *
 * **mutate** - это функция, которая вызывает запрос на сервер, она принимает параматры, описанные ниже.
 */
export const useFetchMutation = <AxiosMutate>({
  index,
  onSuccess,
  isModalLoading = true,
  refetchKey,
  body,
}: Omit<IFetchMutatuion, "url" | "method">) => {
  const { setResponse } = useContext(responseContext);
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: index,
    mutationFn: async ({
      url,
      method,
      body: mutationBody,
    }: Omit<
      IFetchMutatuion,
      "index" | "isModalLoading" | "onSuccess" | "refetchKey"
    >) => {
      isModalLoading && setResponse({ isLoading: true });
      return await axiosBase<AxiosMutate>({
        url,
        method,
        data: mutationBody ? mutationBody : body ? body : null,
      }).then(({ data }) => data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries(refetchKey);
      isModalLoading && setResponse({ isLoading: false });
      onSuccess && onSuccess();
    },
    onError: ({ response }: IError) => {
      setResponse({ errorMessage: response.data.detail });
    },
  });
};
