<template>

  <div class="grid grid-cols-5 grid-rows-5 gap-4">
    <!-- toolbar -->
    <div class="col-span-5">
      <div class="flex items-center gap-2">

        <div class="relative flex-1 min-w-0">
          <MagnifyingGlassIcon class="size-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input class="w-full rounded-md border border-gray-300 py-2 pl-10 pr-3" type="search" name="q"
            placeholder="Search..." aria-label="Search through site content" />
        </div>

        <FolderPlusIcon class="size-7" />
        <DocumentPlusIcon class="size-7" />
      </div>

    </div>

    <!-- profile list -->
    <div class="col-span-5 row-span-4 row-start-2">
      <div v-for="folder in folderList">
        <p>{{ folder.folderName }}</p>
      </div>

    </div>
  </div>


</template>

<script lang="ts" setup>
import { FolderPlusIcon, DocumentPlusIcon, MagnifyingGlassIcon } from '@heroicons/vue/24/outline'
import { useProfileStore, useFolderStore } from '../stores'
const profileStore = useProfileStore()
const folderStore = useFolderStore()
const folderList = folderStore.folderList
console.log("folder list ", folderList)
</script>

<style></style>