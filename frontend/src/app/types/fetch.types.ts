export interface IError {
  response: {
    status: number;
    data: {
      detail: string;
    };
  };
}

export interface IFetchQuery {
  url: string;
  index: any;
  onSuccess?: () => void;
  isModalLoading?: boolean;
  enabled?: boolean;
}

export interface IFetchMutatuion extends Partial<IFetchQuery> {
  refetchKey?: any;
  method: "POST" | "PUT" | "DELETE" | "PATCH";
  body?: any;
}
