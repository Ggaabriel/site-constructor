import { useEffect } from "react";
import { AppRoute } from "./app/routes/AppRoute";
import { telegram } from "./app/tg";
import { useAppDispatch } from "./app/hooks/useAppDispatch";
import { getUser } from "./app/store/slice/UserSlice/userApi";
import { MenuProvider } from "./app/providers/MenuProvider";
import { ResposeProvider } from "./app/providers/ResponseProvider";

function App() {
  const dispatch = useAppDispatch();

  useEffect(() => {
    telegram.windowInitiate();
    dispatch(getUser(telegram.user.id));
  }, []);
  return (
    <>
      <ResposeProvider>
        <MenuProvider>
          <AppRoute />
        </MenuProvider>
      </ResposeProvider>
    </>
  );
}

export default App;
