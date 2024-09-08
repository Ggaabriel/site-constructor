import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

import { responseContext } from "../context";
import Loader from "src/app/assets/loader.svg?react";

const ResposeProvider = ({ children }: { children: React.ReactNode }) => {
  const [response, setResponse] = useState<{
    errorMessage?: string;
    refetchFunc?: () => void;
    isLoading?: boolean;
    // isSuccess?: boolean;
  }>({
    errorMessage: "",
    refetchFunc: () => {},
    isLoading: false,
    // isSuccess: false,
  });

  if (response.errorMessage) {
    setTimeout(() => setResponse({ ...response, errorMessage: "" }), 3000);
  }
  return (
    <responseContext.Provider value={{ response, setResponse }}>
      <AnimatePresence>
        {response.errorMessage && (
          <motion.div
            initial={{ y: "-100%", opacity: 0, translateX: "-50%" }}
            animate={{ y: 0, opacity: 1, translateX: "-50%" }}
            exit={{ y: "-100%", opacity: 0, translateX: "-50%" }}
            className="fixed top-4 left-1/2 rounded-20 font-medium p-4 text-white bg-red-400 z-50"
          >
            {response.errorMessage}
          </motion.div>
        )}
        {response.isLoading && (
          <div className="fixed w-full h-screen bg-black/50 flex justify-center items-center z-50">
            <Loader />
          </div>
        )}
      </AnimatePresence>
      {children}
    </responseContext.Provider>
  );
};

export { ResposeProvider };
