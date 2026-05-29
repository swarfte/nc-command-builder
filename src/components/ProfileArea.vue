<template>
  <div class="h-full flex flex-col bg-gray-50">
    <!-- toolbar -->
    <div class="p-3 border-b border-gray-200">
      <div class="relative">
        <MagnifyingGlassIcon class="size-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
        <input
          class="w-full rounded-md border border-gray-300 py-2 pl-10 pr-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          type="search" name="q" placeholder="Search profiles..." aria-label="Search through profiles" />

      </div>
    </div>


    <!-- sidebar content -->
    <div
      class="flex-1 overflow-y-auto p-2 relative bg-gray-50"
      @contextmenu.self.prevent="handleSidebarContextMenu"
    >
      <div v-for="folder in folderList" :key="folder.id" class="mb-1">
        <!-- folder header -->
        <div class="flex items-center gap-2 p-2 rounded hover:bg-gray-200 cursor-pointer group"
          @click="toggleFolder(folder.id)" @contextmenu.prevent="handleFolderContextMenu($event, folder)">
          <ChevronRightIcon :class="[
            'size-4 transition-transform',
            expandedFolders.has(folder.id) ? 'rotate-90' : ''
          ]" />
          <FolderIcon class="size-5 text-yellow-500" />
          <span class="flex-1 text-sm font-medium text-gray-700">{{ folder.folderName }}</span>
          <span class="text-xs text-gray-400">{{ folder.profiles.length }}</span>
        </div>

        <!-- folder content (profiles) -->
        <div v-if="expandedFolders.has(folder.id)" class="ml-6 mt-1 space-y-0.5">
          <div v-for="profile in folder.profiles" :key="profile.id"
            class="flex items-center gap-2 p-2 rounded hover:bg-gray-200 cursor-pointer group"
            :class="{ 'bg-blue-100': currentProfile?.id === profile.id }" @click="loadProfile(profile)"
            @contextmenu.prevent="handleProfileContextMenu($event, folder, profile)">
            <DocumentIcon class="size-4 text-gray-500" />
            <span class="flex-1 text-sm text-gray-700 truncate">{{ profile.profileName }}</span>
          </div>

          <!-- empty state -->
          <div v-if="folder.profiles.length === 0" class="p-2 text-sm text-gray-400 italic"
            @contextmenu.prevent="handleFolderContextMenu($event, folder)">
            Empty folder
          </div>
        </div>
      </div>
    </div>

    <!-- overlay to close context menu -->
    <div v-if="contextMenu.show" class="fixed inset-0 z-[9998]" @click="closeContextMenu" />

    <!-- context menu -->
    <div v-if="contextMenu.show"
      class="fixed bg-white rounded-lg shadow-xl border border-gray-200 py-1 z-[9999] min-w-[160px]"
      :style="{ top: contextMenu.y + 'px', left: contextMenu.x + 'px' }">
      <button v-if="contextMenu.options.showNewProfile"
        class="w-full px-4 py-2 text-left text-sm hover:bg-gray-100 flex items-center gap-2" @click="handleNewProfile">
        <DocumentPlusIcon class="size-4" />
        <span>New Profile</span>
      </button>

      <button v-if="contextMenu.options.showNewFolder"
        class="w-full px-4 py-2 text-left text-sm hover:bg-gray-100 flex items-center gap-2" @click="handleNewFolder">
        <FolderPlusIcon class="size-4" />
        <span>New Folder</span>
      </button>
    </div>

    <!-- new folder dialog -->
    <div v-if="showNewFolderDialog" class="fixed inset-0 z-[10000] flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white rounded-lg shadow-xl p-6 w-96">
        <h3 class="text-lg font-semibold mb-4">Create New Folder</h3>
        <input ref="folderNameInput" v-model="newFolderName"
          class="w-full rounded-md border border-gray-300 px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          type="text" placeholder="Enter folder name" @keyup.enter="confirmNewFolder" @keyup.esc="cancelNewFolder" />
        <div class="flex justify-end gap-2">
          <button class="px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md" @click="cancelNewFolder">
            Cancel
          </button>
          <button class="px-4 py-2 text-sm bg-blue-500 text-white hover:bg-blue-600 rounded-md"
            @click="confirmNewFolder">
            Create
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import {
  FolderPlusIcon,
  DocumentPlusIcon,
  MagnifyingGlassIcon,
  FolderIcon,
  DocumentIcon,
  ChevronRightIcon
} from '@heroicons/vue/24/outline'
import { useProfileStore, useFolderStore } from '../stores'
import type { Profile, Folder } from '../models'

const profileStore = useProfileStore()
const folderStore = useFolderStore()

const currentProfile = computed(() => profileStore.currentProfile)
const folderList = computed(() => folderStore.folderList)

// Track expanded folders
const expandedFolders = ref<Set<string>>(new Set(['General']))

// Context menu state
interface ContextMenuOptions {
  showNewProfile: boolean
  showNewFolder: boolean
}

interface ContextMenuState {
  show: boolean
  x: number
  y: number
  options: ContextMenuOptions
  targetFolder?: Folder
}

const contextMenu = ref<ContextMenuState>({
  show: false,
  x: 0,
  y: 0,
  options: {
    showNewProfile: false,
    showNewFolder: false,
  },
  targetFolder: undefined,
})

// New folder dialog state
const showNewFolderDialog = ref(false)
const newFolderName = ref('')
const folderNameInput = ref<HTMLInputElement | null>(null)

// Toggle folder expansion
const toggleFolder = (folderId: string) => {
  if (expandedFolders.value.has(folderId)) {
    expandedFolders.value.delete(folderId)
  } else {
    expandedFolders.value.add(folderId)
  }
  expandedFolders.value = new Set(expandedFolders.value) // Trigger reactivity
}

// Load profile into current profile
const loadProfile = (profile: Profile) => {
  profileStore.loadProfile(profile)
}

// Close context menu
const closeContextMenu = () => {
  contextMenu.value.show = false
}

// Handle sidebar context menu (empty area)
const handleSidebarContextMenu = (event: MouseEvent) => {
  console.log('Sidebar context menu triggered')
  const generalFolder = folderList.value.find(f => f.folderName === 'General')

  contextMenu.value = {
    show: true,
    x: event.clientX,
    y: event.clientY,
    options: {
      showNewProfile: !!generalFolder,
      showNewFolder: true,
    },
    targetFolder: generalFolder,
  }

  console.log('Context menu state:', contextMenu.value)
}

// Handle folder context menu
const handleFolderContextMenu = (event: MouseEvent, folder: Folder) => {
  contextMenu.value = {
    show: true,
    x: event.clientX,
    y: event.clientY,
    options: {
      showNewProfile: true,
      showNewFolder: false,
    },
    targetFolder: folder,
  }
}

// Handle profile context menu
const handleProfileContextMenu = (event: MouseEvent, folder: Folder, profile: Profile) => {
  contextMenu.value = {
    show: true,
    x: event.clientX,
    y: event.clientY,
    options: {
      showNewProfile: true,
      showNewFolder: false,
    },
    targetFolder: folder,
  }
}

// Handle new profile creation
const handleNewProfile = () => {
  if (contextMenu.value.targetFolder) {
    const newProfile: Profile = {
      id: crypto.randomUUID(),
      version: "1.0",
      profileName: "New Profile",
      host: "localhost",
      port: 8080,
      targetMode: "connect",
      protocol: "TCP",
      flavor: "GNU netcat",
      payloadMode: "GET",
      outputType: "printf",
      contentType: "text/plain",
      connection: "close",
      isVerbose: true,
      isNoDNS: false,
      isKeepListening: true,
      timeout: 5,
      closeDelay: 0,
      bindCommand: "",
    }

    folderStore.addProfileToFolder(contextMenu.value.targetFolder.folderName, newProfile)

    // Expand the folder to show the new profile
    expandedFolders.value.add(contextMenu.value.targetFolder.id)
    expandedFolders.value = new Set(expandedFolders.value)

    // Load the new profile
    profileStore.loadProfile(newProfile)
  }

  closeContextMenu()
}

// Handle new folder creation
const handleNewFolder = () => {
  closeContextMenu()
  showNewFolderDialog.value = true
  newFolderName.value = ''

  // Focus the input field after the dialog is shown
  setTimeout(() => {
    folderNameInput.value?.focus()
  }, 100)
}

const confirmNewFolder = () => {
  if (newFolderName.value.trim()) {
    try {
      folderStore.addFolder(newFolderName.value.trim())
      showNewFolderDialog.value = false
      newFolderName.value = ''
    } catch (error) {
      alert(error instanceof Error ? error.message : 'Failed to create folder')
    }
  } else {
    alert('Please enter a folder name')
  }
}

const cancelNewFolder = () => {
  showNewFolderDialog.value = false
  newFolderName.value = ''
}
</script>