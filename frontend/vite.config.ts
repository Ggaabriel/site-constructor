import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import svgr from "vite-plugin-svgr";

export default defineConfig({
  plugins: [
    svgr({
      include: "**/*.svg?react",
    }),
    react(),
  ],
  base: "/",
  preview: {
    host: true,
    port: 5173,
  },
  server: {
    host: true,
  },
  resolve: {
    alias: {
      src: "/src",
    },
  },
});
