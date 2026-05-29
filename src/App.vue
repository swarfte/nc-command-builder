<script setup lang="ts">
import ProfileArea from "./components/profileArea.vue";
import PayloadArea from "./components/payloadArea.vue";
import PreviewArea from "./components/PreviewArea.vue";
import ConfigArea from "./components/ConfigArea.vue";

</script>

<template>

  <div className="grid grid-cols-5 grid-rows-7 gap-4">
    <div className="row-span-7">
      <ProfileArea />
    </div>
    <div className="col-span-4">
      <ConfigArea />
    </div>
    <div className="col-span-4 row-span-4 col-start-2 row-start-2">
      <PayloadArea />
    </div>
    <div className="col-span-4 row-span-2 col-start-2 row-start-6">
      <PreviewArea />
    </div>
  </div>

</template>
