import { Dispatch, SetStateAction, createContext } from "react";
import { IMenu } from "src/widgets/Menu/MenuModel";
import { menuItem } from "../routes/menuListItem";

interface IMenuContext {
  menuItems: IMenu[];
  setMenuItems: Dispatch<SetStateAction<IMenu[]>>;
}

interface IResponseContext {
  response: {
    errorMessage?: string;
    refetchFunc?: () => void;
    isLoading?: boolean;
    isSuccess?: boolean;
  };
  setResponse: React.Dispatch<
    React.SetStateAction<{
      errorMessage?: string;
      refetchFunc?: () => void;
      isLoading?: boolean;
      isSuccess?: boolean;
    }>
  >;
}
/** **menuContext** - это контект для изменения меню навигации */
export const menuContext = createContext<IMenuContext>({
  menuItems: menuItem,
  setMenuItems: () => {},
});

/** **responseContext** - это контекст отвечающий за отображение, компонентов при ожидании ответа от сервера и приходящих с него ошибок.
 *
 * **isLoading** - это булевое значение, которое отвечает за отображение моального окна загрузки при ожидании ответа от сервера.
 *
 * **errorMessage** - это строка, которая отображается в pop up окне с передаваемым внутрь сообщением о том, что произошла ошибка при запросе или она пришла с сервера.
 *
 * **refetchFunc** - это функция, которая срабатывает при возврещении ошибки с сервера.
 *
 * **setResponse** - это функция, которая изменяет все состояния, описаные выше.
 */

export const responseContext = createContext<IResponseContext>({
  response: {
    errorMessage: "",
    refetchFunc: () => {},
    isLoading: false,
    // isSuccess: false,
  },
  setResponse: () => {},
});
