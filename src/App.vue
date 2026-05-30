<script setup lang="ts">
import ProfileArea from "./components/ProfileArea.vue";
import PayloadArea from "./components/PayloadArea.vue";
import PreviewArea from "./components/PreviewArea.vue";
import ConfigArea from "./components/ConfigArea.vue";

</script>

<template>

  <div class="grid grid-cols-12 gap-2 items-start min-h-screen">
    <div class="col-span-2 row-span-3">
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
