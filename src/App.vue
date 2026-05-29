<script setup lang="ts">
import ProfileArea from "./components/ProfileArea.vue";
import PayloadArea from "./components/PayloadArea.vue";
import PreviewArea from "./components/PreviewArea.vue";
import ConfigArea from "./components/ConfigArea.vue";

</script>

<template>
  <div class="grid grid-cols-12 grid-rows-9 gap-4">
    <div class="col-span-3 row-span-9">
      <ProfileArea />
    </div>
    <div class="col-span-9 row-span-2 col-start-4">
      <ConfigArea />
    </div>
    <div class="col-span-9 row-span-4 col-start-4 row-start-3">
      <PayloadArea />
    </div>
    <div class="col-span-9 row-span-3 col-start-4 row-start-7">
      <PreviewArea />
    </div>
  </div>

</template>
