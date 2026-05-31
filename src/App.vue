<script setup lang="ts">
import ProfileArea from "./components/ProfileArea.vue";
import PayloadArea from "./components/PayloadArea.vue";
import PreviewArea from "./components/PreviewArea.vue";
import ConfigArea from "./components/ConfigArea.vue";

</script>

<template>

  <div class="relative grid grid-cols-12 gap-2 items-stretch min-h-screen">
    <a class="absolute right-3 top-3 inline-flex size-9 items-center justify-center rounded-full border border-gray-200 bg-white text-gray-700 shadow-sm transition hover:border-gray-300 hover:text-gray-900"
      href="https://github.com/swarfte/nc-command-builder" target="_blank" rel="noopener noreferrer"
      aria-label="Open GitHub repository" title="Open GitHub repository">
      <svg viewBox="0 0 24 24" aria-hidden="true" class="size-5" fill="currentColor">
        <path
          d="M12 2C6.48 2 2 6.58 2 12.26c0 4.54 2.87 8.38 6.84 9.74.5.1.68-.22.68-.48 0-.24-.01-.88-.01-1.73-2.78.62-3.37-1.38-3.37-1.38-.46-1.2-1.11-1.52-1.11-1.52-.91-.64.07-.63.07-.63 1 .07 1.53 1.05 1.53 1.05.9 1.57 2.36 1.12 2.94.86.09-.67.35-1.12.64-1.38-2.22-.26-4.56-1.14-4.56-5.05 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.3.1-2.7 0 0 .84-.28 2.75 1.05A9.2 9.2 0 0 1 12 6.8c.85 0 1.71.12 2.51.34 1.91-1.33 2.75-1.05 2.75-1.05.55 1.4.2 2.44.1 2.7.64.72 1.03 1.63 1.03 2.75 0 3.92-2.34 4.78-4.57 5.03.36.32.68.94.68 1.9 0 1.38-.01 2.5-.01 2.84 0 .26.18.58.69.48 3.97-1.36 6.83-5.2 6.83-9.74C22 6.58 17.52 2 12 2Z" />
      </svg>
    </a>
    <div class="col-span-2 row-span-3 bg-gray-50 min-h-screen h-full">
      <ProfileArea />
    </div>
    <div class="col-span-10">
      <ConfigArea />
    </div>
    <div class="col-span-10">
      <PayloadArea />
    </div>
    <div class="col-span-10">
      <PreviewArea />
    </div>
  </div>

</template>
