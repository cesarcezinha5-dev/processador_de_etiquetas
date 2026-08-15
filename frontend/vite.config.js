import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],

  server: {
    proxy: {
      "/processar": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
      },

      "/status": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
      },

      "/downloads": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
      },
    },
  },
});