import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";
import tailwindcss from "@tailwindcss/vite";
import checker from "vite-plugin-checker";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vueDevTools(),
    vue(),
    tailwindcss(),
    checker({
      // Instructs the plugin to use vue-tsc for template and TS analysis
      vueTsc: true,
    }),
  ],
});
