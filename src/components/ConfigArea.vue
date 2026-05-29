<template>
  <div class="h-full flex flex-col bg-white">
    <div class="flex-1 overflow-y-auto p-4">
      <div class="w-full">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">Configuration</h2>

        <!-- Basic Configuration -->
        <div class="mb-4">
          <!-- <h3 class="text-xs font-medium text-gray-600 mb-2 uppercase tracking-wide">Basic</h3> -->
          <div class="grid grid-cols-5 gap-2">
            <!-- Host -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Host</label>
              <input v-model="localConfig.host"
                class="w-full rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                type="text" placeholder="localhost" />
            </div>

            <!-- Port -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Port</label>
              <input v-model.number="localConfig.port"
                class="w-full rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                type="number" placeholder="8080" />
            </div>

            <!-- Operation Mode -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Mode</label>
              <select v-model="localConfig.targetMode"
                class="w-full rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500">
                <option value="connect">Connect</option>
                <option value="listen">Listen</option>
              </select>
            </div>

            <!-- Protocol -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Protocol</label>
              <select v-model="localConfig.protocol"
                class="w-full rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500">
                <option value="TCP">TCP</option>
                <option value="UDP">UDP</option>
              </select>
            </div>

            <!-- NC Flavor -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Netcat Flavor</label>
              <select v-model="localConfig.flavor"
                class="w-full rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500">
                <option value="GNU netcat">GNU netcat</option>
                <option value="OpenBSD netcat">OpenBSD netcat</option>
                <option value="Netcat from FreeBSD">Netcat from FreeBSD</option>
                <option value="Ncat (Nmap)">Ncat (Nmap)</option>
                <option value="socat">socat</option>
              </select>
            </div>
          </div>
        </div>



        <!-- Advanced Options -->
        <div class="mb-4">
          <!-- <h3 class="text-xs font-medium text-gray-600 mb-2 uppercase tracking-wide">Advanced</h3> -->
          <div class="grid grid-cols-3 gap-2">
            <!-- Timeout -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Timeout</label>
              <div class="relative">
                <input v-model.number="localConfig.timeout"
                  class="w-full rounded border border-gray-300 px-2 py-1.5 pr-8 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  type="number" placeholder="5" />
                <span class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-gray-400">-w</span>
              </div>
            </div>

            <!-- Close Delay -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Close Delay</label>
              <div class="relative">
                <input v-model.number="localConfig.closeDelay"
                  class="w-full rounded border border-gray-300 px-2 py-1.5 pr-8 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  type="number" placeholder="0" />
                <span class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-gray-400">-q</span>
              </div>
            </div>

            <!-- Bind Script -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Bind Script</label>
              <div class="relative">
                <input v-model="localConfig.bindCommand"
                  class="w-full rounded border border-gray-300 px-2 py-1.5 pr-8 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  type="text" placeholder="shell command" />
                <span class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-gray-400">-s</span>
              </div>
            </div>
          </div>
        </div>
        <!-- Network Options -->
        <div class="mb-4">
          <!-- <h3 class="text-xs font-medium text-gray-600 mb-2 uppercase tracking-wide">Network</h3> -->
          <div class="grid grid-cols-3 gap-2">
            <!-- Verbose -->
            <label class="flex items-center gap-2 p-2 rounded border border-gray-200 hover:bg-gray-50 cursor-pointer">
              <input v-model="localConfig.isVerbose"
                class="size-3.5 rounded border-gray-300 text-blue-600 focus:ring-blue-500" type="checkbox" />
              <div class="flex-1">
                <span class="text-xs font-medium text-gray-700">Verbose</span>
                <span class="ml-1 text-xs text-gray-400">(-v)</span>
              </div>
            </label>

            <!-- No DNS -->
            <label class="flex items-center gap-2 p-2 rounded border border-gray-200 hover:bg-gray-50 cursor-pointer">
              <input v-model="localConfig.isNoDNS"
                class="size-3.5 rounded border-gray-300 text-blue-600 focus:ring-blue-500" type="checkbox" />
              <div class="flex-1">
                <span class="text-xs font-medium text-gray-700">No DNS</span>
                <span class="ml-1 text-xs text-gray-400">(-n)</span>
              </div>
            </label>

            <!-- Keep Listening -->
            <label class="flex items-center gap-2 p-2 rounded border border-gray-200 hover:bg-gray-50 cursor-pointer">
              <input v-model="localConfig.isKeepListening"
                class="size-3.5 rounded border-gray-300 text-blue-600 focus:ring-blue-500" type="checkbox" />
              <div class="flex-1">
                <span class="text-xs font-medium text-gray-700">Keep Listening</span>
                <span class="ml-1 text-xs text-gray-400">(-k)</span>
              </div>
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch, onMounted } from 'vue'
import { useProfileStore, useFolderStore } from '../stores'

const profileStore = useProfileStore()
const folderStore = useFolderStore()

// Flag to prevent circular updates
const isUpdatingFromStore = ref(false)

// Local config state with only the fields we're editing
const localConfig = ref({
  host: 'localhost',
  port: 8080,
  targetMode: 'connect',
  protocol: 'TCP',
  flavor: 'GNU netcat',
  isVerbose: true,
  isNoDNS: false,
  isKeepListening: true,
  timeout: 5,
  closeDelay: 0,
  bindCommand: '',
})

// Load current profile into local config
const loadCurrentProfile = () => {
  isUpdatingFromStore.value = true
  const profile = profileStore.currentProfile
  localConfig.value = {
    host: profile.host,
    port: profile.port,
    targetMode: profile.targetMode,
    protocol: profile.protocol,
    flavor: profile.flavor,
    isVerbose: profile.isVerbose,
    isNoDNS: profile.isNoDNS,
    isKeepListening: profile.isKeepListening,
    timeout: profile.timeout,
    closeDelay: profile.closeDelay || 0,
    bindCommand: profile.bindCommand || '',
  }
  // Reset flag after a small delay to prevent immediate trigger
  setTimeout(() => {
    isUpdatingFromStore.value = false
  }, 50)
}

// Find the folder that contains the current profile
const findFolderForProfile = (profileId: string) => {
  return folderStore.folderList.find(folder =>
    folder.profiles.some(profile => profile.id === profileId)
  )
}

// Watch local config changes and update both stores
watch(localConfig, (newConfig) => {
  if (!isUpdatingFromStore.value) {
    // Update current profile in profile store
    profileStore.updateProfile(newConfig)

    // Also update the profile in the folder store
    const currentProfileId = profileStore.currentProfile.id
    const folder = findFolderForProfile(currentProfileId)

    if (folder) {
      // Update the profile in the folder with the new config values
      const updatedProfile = {
        ...profileStore.currentProfile,
        ...newConfig
      }
      folderStore.updateProfileInFolder(folder.id, updatedProfile)
    }
  }
}, { deep: true })

// Watch for profile changes from other components (like switching profiles)
watch(() => profileStore.currentProfile, () => {
  loadCurrentProfile()
}, { deep: true })

// Load current profile on mount
onMounted(() => {
  loadCurrentProfile()
})
</script>

<style></style>