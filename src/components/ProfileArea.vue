<template>
  <div class="h-full flex flex-col bg-gray-50">
    <!-- toolbar -->
    <div class="p-3 border-b border-gray-200">
      <div class="relative flex items-center gap-2">
        <div class="relative flex-1">
          <MagnifyingGlassIcon class="size-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            class="w-full rounded-md border border-gray-300 py-2 pl-10 pr-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            type="search" name="q" placeholder="Search profiles..." aria-label="Search through profiles" />
        </div>
        <button class="px-3 py-2 text-sm bg-red-500 text-white hover:bg-red-600 rounded-md flex items-center gap-2"
          @click="showResetConfirmDialog = true">
          <ArrowPathIcon class="size-5" />
        </button>
      </div>
    </div>


    <!-- sidebar content -->
    <div class="flex-1 overflow-y-auto p-2 relative bg-gray-50" @contextmenu.prevent="handleSidebarContextMenu">
      <div v-for="folder in folderList" :key="folder.id" class="mb-1">
        <!-- folder header -->
        <div class="flex items-center gap-2 p-2 rounded hover:bg-gray-200 cursor-pointer group"
          @click="toggleFolder(folder.id)" @contextmenu.stop.prevent="handleFolderContextMenu($event, folder)">
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
            @contextmenu.stop.prevent="handleProfileContextMenu($event, folder, profile)">
            <DocumentIcon class="size-4 text-gray-500" />
            <span class="flex-1 text-sm text-gray-700 truncate">{{ profile.profileName }}</span>
          </div>

          <!-- empty state -->
          <div v-if="folder.profiles.length === 0" class="p-2 text-sm text-gray-400 italic"
            @contextmenu.stop.prevent="handleFolderContextMenu($event, folder)">
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

      <!-- <div v-if="contextMenu.options.showDuplicate || contextMenu.options.showRename || contextMenu.options.showDelete"
        class="border-t border-gray-200 my-1"></div> -->

      <button v-if="contextMenu.options.showDuplicate"
        class="w-full px-4 py-2 text-left text-sm hover:bg-gray-100 flex items-center gap-2" @click="handleDuplicate">
        <DocumentDuplicateIcon v-if="contextMenu.targetProfile" class="size-4" />
        <FolderIcon v-else class="size-4" />
        <span>Duplicate</span>
      </button>

      <button v-if="contextMenu.options.showRename"
        class="w-full px-4 py-2 text-left text-sm hover:bg-gray-100 flex items-center gap-2" @click="handleRename">
        <PencilIcon class="size-4" />
        <span>Rename</span>
      </button>

      <button v-if="contextMenu.options.showDelete"
        class="w-full px-4 py-2 text-left text-sm hover:bg-red-50 text-red-600 flex items-center gap-2"
        @click="handleDelete">
        <TrashIcon class="size-4" />
        <span>Delete</span>
      </button>
    </div>

    <!-- new folder dialog -->
    <div v-if="showNewFolderDialog"
      class="fixed inset-0 z-[10000] flex items-center justify-center bg-black bg-opacity-50">
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

    <!-- rename profile dialog -->
    <div v-if="showRenameProfileDialog"
      class="fixed inset-0 z-[10000] flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white rounded-lg shadow-xl p-6 w-96">
        <h3 class="text-lg font-semibold mb-4">Rename Profile</h3>
        <input ref="renameProfileInput" v-model="renameProfileName"
          class="w-full rounded-md border border-gray-300 px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          type="text" placeholder="Enter profile name" @keyup.enter="confirmRenameProfile"
          @keyup.esc="cancelRenameProfile" />
        <div class="flex justify-end gap-2">
          <button class="px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md" @click="cancelRenameProfile">
            Cancel
          </button>
          <button class="px-4 py-2 text-sm bg-blue-500 text-white hover:bg-blue-600 rounded-md"
            @click="confirmRenameProfile">
            Rename
          </button>
        </div>
      </div>
    </div>

    <!-- rename folder dialog -->
    <div v-if="showRenameFolderDialog"
      class="fixed inset-0 z-[10000] flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white rounded-lg shadow-xl p-6 w-96">
        <h3 class="text-lg font-semibold mb-4">Rename Folder</h3>
        <input ref="renameFolderInput" v-model="renameFolderName"
          class="w-full rounded-md border border-gray-300 px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          type="text" placeholder="Enter folder name" @keyup.enter="confirmRenameFolder"
          @keyup.esc="cancelRenameFolder" />
        <div class="flex justify-end gap-2">
          <button class="px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md" @click="cancelRenameFolder">
            Cancel
          </button>
          <button class="px-4 py-2 text-sm bg-blue-500 text-white hover:bg-blue-600 rounded-md"
            @click="confirmRenameFolder">
            Rename
          </button>
        </div>
      </div>
    </div>

    <!-- reset confirmation dialog -->
    <div v-if="showResetConfirmDialog"
      class="fixed inset-0 z-[10000] flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white rounded-lg shadow-xl p-6 w-96">
        <h3 class="text-lg font-semibold mb-4">Reset All Data</h3>
        <p class="text-sm text-gray-600 mb-6">
          Are you sure you want to reset all data? This will delete all folders and profiles except the General folder
          and default profile. This action cannot be undone.
        </p>
        <div class="flex justify-end gap-2">
          <button class="px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md" @click="cancelReset">
            Cancel
          </button>
          <button class="px-4 py-2 text-sm bg-red-500 text-white hover:bg-red-600 rounded-md" @click="confirmReset">
            Reset All
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import {
  FolderPlusIcon,
  DocumentPlusIcon,
  MagnifyingGlassIcon,
  FolderIcon,
  DocumentIcon,
  ChevronRightIcon,
  DocumentDuplicateIcon,
  PencilIcon,
  TrashIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'
import { useProfileStore, useFolderStore } from '../stores'
import type { Profile, Folder } from '../models'

const profileStore = useProfileStore()
const folderStore = useFolderStore()

const currentProfile = computed(() => profileStore.currentProfile)
const folderList = computed(() => folderStore.folderList)

// Track expanded folders
const expandedFolders = ref<Set<string>>(new Set(['-1'])) // -1 is the General folder ID

// Context menu state
interface ContextMenuOptions {
  showNewProfile: boolean
  showNewFolder: boolean
  showDuplicate: boolean
  showRename: boolean
  showDelete: boolean
}

interface ContextMenuState {
  show: boolean
  x: number
  y: number
  options: ContextMenuOptions
  targetFolder?: Folder
  targetProfile?: Profile
}

const contextMenu = ref<ContextMenuState>({
  show: false,
  x: 0,
  y: 0,
  options: {
    showNewProfile: false,
    showNewFolder: false,
    showDuplicate: false,
    showRename: false,
    showDelete: false,
  },
  targetFolder: undefined,
  targetProfile: undefined,
})

// New folder dialog state
const showNewFolderDialog = ref(false)
const newFolderName = ref('')
const folderNameInput = ref<HTMLInputElement | null>(null)

// Rename dialogs state
const showRenameProfileDialog = ref(false)
const showRenameFolderDialog = ref(false)
const renameProfileName = ref('')
const renameFolderName = ref('')
const renameProfileInput = ref<HTMLInputElement | null>(null)
const renameFolderInput = ref<HTMLInputElement | null>(null)

// Reset confirmation dialog state
const showResetConfirmDialog = ref(false)

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
  const generalFolder = folderStore.getFolderById('-1') // Get General folder by ID

  contextMenu.value = {
    show: true,
    x: event.clientX,
    y: event.clientY,
    options: {
      showNewProfile: !!generalFolder,
      showNewFolder: true,
      showDuplicate: false,
      showRename: false,
      showDelete: false,
    },
    targetFolder: generalFolder || undefined,
  }

  console.log('Context menu state:', contextMenu.value)
}

// Handle folder context menu
const handleFolderContextMenu = (event: MouseEvent, folder: Folder) => {
  const isGeneralFolder = folder.id === '-1' // General folder has ID "-1"

  contextMenu.value = {
    show: true,
    x: event.clientX,
    y: event.clientY,
    options: {
      showNewProfile: true,
      showNewFolder: false,
      showDuplicate: true,      // Can duplicate any folder including General
      showRename: true,         // Can rename any folder including General
      showDelete: !isGeneralFolder, // Only restriction: can't delete General folder
    },
    targetFolder: folder,
    targetProfile: undefined,
  }
}

// Handle profile context menu
const handleProfileContextMenu = (event: MouseEvent, folder: Folder, profile: Profile) => {
  const isDefaultProfile = profile.id === 'default-profile' && folder.id === '-1'

  contextMenu.value = {
    show: true,
    x: event.clientX,
    y: event.clientY,
    options: {
      showNewProfile: false,
      showNewFolder: false,
      showDuplicate: true,      // Can duplicate any profile including default
      showRename: true,         // Can rename any profile including default
      showDelete: !isDefaultProfile, // Only restriction: can't delete default profile
    },
    targetFolder: folder,
    targetProfile: profile,
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
      path: "",
      targetMode: "connect",
      protocol: "TCP",
      flavor: "GNU netcat",
      userAgent: "nc-command-builder",
      payloadMode: "GET",
      outputType: "printf",
      contentType: "text/plain",
      connection: "close",
      cookie: "",
      isVerbose: true,
      isNoDNS: false,
      isKeepListening: true,
      timeout: 5,
      closeDelay: 0,
      bindCommand: "",
    }

    folderStore.addProfileToFolder(contextMenu.value.targetFolder.id, newProfile)

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

// Handle duplicate
const handleDuplicate = () => {
  if (contextMenu.value.targetProfile) {
    // Duplicate profile
    const profile = contextMenu.value.targetProfile
    const newProfile: Profile = {
      ...profile,
      id: crypto.randomUUID(),
      profileName: `${profile.profileName} (copy)`,
    }

    if (contextMenu.value.targetFolder) {
      folderStore.addProfileToFolder(contextMenu.value.targetFolder.id, newProfile)
      expandedFolders.value.add(contextMenu.value.targetFolder.id)
      expandedFolders.value = new Set(expandedFolders.value)
    }
  } else if (contextMenu.value.targetFolder) {
    // Duplicate folder
    const folder = contextMenu.value.targetFolder
    const newFolderName = `${folder.folderName} (copy)`

    try {
      // Create new folder
      const newFolder = folderStore.addFolder(newFolderName)

      // Copy all profiles to the new folder
      folder.profiles.forEach(profile => {
        const newProfile: Profile = {
          ...profile,
          id: crypto.randomUUID(),
        }
        folderStore.addProfileToFolder(newFolder.id, newProfile)
      })

      // Expand the new folder
      expandedFolders.value.add(newFolder.id)
      expandedFolders.value = new Set(expandedFolders.value)
    } catch (error) {
      alert(error instanceof Error ? error.message : 'Failed to duplicate folder')
    }
  }

  closeContextMenu()
}

// Handle rename
const handleRename = () => {
  closeContextMenu()

  if (contextMenu.value.targetProfile) {
    showRenameProfileDialog.value = true
    renameProfileName.value = contextMenu.value.targetProfile.profileName
    setTimeout(() => {
      renameProfileInput.value?.focus()
    }, 100)
  } else if (contextMenu.value.targetFolder) {
    showRenameFolderDialog.value = true
    renameFolderName.value = contextMenu.value.targetFolder.folderName
    setTimeout(() => {
      renameFolderInput.value?.focus()
    }, 100)
  }
}

const confirmRenameProfile = () => {
  if (renameProfileName.value.trim() && contextMenu.value.targetFolder && contextMenu.value.targetProfile) {
    const updatedProfile: Profile = {
      ...contextMenu.value.targetProfile,
      profileName: renameProfileName.value.trim(),
    }

    folderStore.updateProfileInFolder(contextMenu.value.targetFolder.id, updatedProfile)

    // If this is the current profile, update it too
    if (profileStore.currentProfile.id === contextMenu.value.targetProfile.id) {
      profileStore.loadProfile(updatedProfile)
    }

    showRenameProfileDialog.value = false
    renameProfileName.value = ''
  } else {
    alert('Please enter a profile name')
  }
}

const cancelRenameProfile = () => {
  showRenameProfileDialog.value = false
  renameProfileName.value = ''
}

const confirmRenameFolder = () => {
  if (renameFolderName.value.trim() && contextMenu.value.targetFolder) {
    try {
      folderStore.renameFolder(contextMenu.value.targetFolder.id, renameFolderName.value.trim())
      showRenameFolderDialog.value = false
      renameFolderName.value = ''
    } catch (error) {
      alert(error instanceof Error ? error.message : 'Failed to rename folder')
    }
  } else {
    alert('Please enter a folder name')
  }
}

const cancelRenameFolder = () => {
  showRenameFolderDialog.value = false
  renameFolderName.value = ''
}

// Handle delete
const handleDelete = () => {
  if (contextMenu.value.targetProfile && contextMenu.value.targetFolder) {
    // Delete profile
    const isDefaultProfile = contextMenu.value.targetProfile.id === 'default-profile' &&
      contextMenu.value.targetFolder.folderName === 'General'

    if (isDefaultProfile) {
      alert('Cannot delete the default profile.')
      closeContextMenu()
      return
    }

    if (confirm(`Are you sure you want to delete "${contextMenu.value.targetProfile.profileName}"?`)) {
      try {
        folderStore.deleteProfileFromFolder(contextMenu.value.targetFolder.id, contextMenu.value.targetProfile.id)

        // If deleted profile was current, reset to default
        if (profileStore.currentProfile.id === contextMenu.value.targetProfile.id) {
          // Load the default profile from General folder
          const generalFolder = folderStore.getFolderById('-1')
          if (generalFolder && generalFolder.profiles.length > 0) {
            const defaultProfile = generalFolder.profiles.find(p => p.id === 'default-profile')
            if (defaultProfile) {
              profileStore.loadProfile(defaultProfile)
            }
          }
        }
      } catch (error) {
        alert(error instanceof Error ? error.message : 'Failed to delete profile')
      }
    }
  } else if (contextMenu.value.targetFolder) {
    // Delete folder
    if (confirm(`Are you sure you want to delete "${contextMenu.value.targetFolder.folderName}" and all its profiles?`)) {
      try {
        folderStore.deleteFolder(contextMenu.value.targetFolder.id)
      } catch (error) {
        alert(error instanceof Error ? error.message : 'Failed to delete folder')
      }
    }
  }

  closeContextMenu()
}

// Handle reset
const confirmReset = () => {
  // Reset folder store to initial state
  folderStore.folderDict = {
    '-1': {
      id: '-1',
      folderName: 'General',
      profiles: [
        {
          id: 'default-profile',
          version: '1.0',
          profileName: 'default',
          host: 'localhost',
          port: 8080,
          path: '',
          userAgent: 'nc-command-builder',
          targetMode: 'connect',
          protocol: 'TCP',
          flavor: 'GNU netcat',
          payloadMode: 'GET',
          outputType: 'printf',
          query: '',
          body: '',
          cookie: '',
          contentType: 'text/plain',
          connection: 'close',
          isVerbose: true,
          isNoDNS: false,
          isKeepListening: true,
          timeout: 5,
          closeDelay: 0,
          bindCommand: '',
        },
      ],
    },
  }

  // Reset current profile to default
  const generalFolder = folderStore.getFolderById('-1')
  if (generalFolder && generalFolder.profiles.length > 0) {
    const defaultProfile = generalFolder.profiles.find(p => p.id === 'default-profile')
    if (defaultProfile) {
      profileStore.loadProfile(defaultProfile)
    }
  }

  // Reset expanded folders to only show General
  expandedFolders.value = new Set(['-1'])

  showResetConfirmDialog.value = false
}

const cancelReset = () => {
  showResetConfirmDialog.value = false
}

// Initialize default profile on component mount
onMounted(() => {
  // Check if we should load the default profile from General folder
  const generalFolder = folderStore.getFolderById('-1')
  if (generalFolder && generalFolder.profiles.length > 0) {
    const defaultProfile = generalFolder.profiles.find(p => p.id === 'default-profile')
    if (defaultProfile && profileStore.currentProfile.profileName === 'default') {
      // Only load if current profile is still the default one (user hasn't modified it)
      profileStore.loadProfile(defaultProfile)
    }
  }
})
</script>