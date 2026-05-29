<template>
  <div class="h-full flex flex-col bg-white">
    <div class="flex-1 overflow-y-auto p-4">
      <div class="w-full">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">Configuration</h2>

        <!-- Basic Configuration -->
        <div class="mb-4">
          <h3 class="text-xs font-medium text-gray-600 mb-2 uppercase tracking-wide">Basic</h3>
          <div class="grid grid-cols-5 gap-2">
            <!-- Host -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Host</label>
              <input
                v-model="config.host"
                class="w-full rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                type="text" placeholder="localhost" />
            </div>

            <!-- Port -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Port</label>
              <input
                v-model.number="config.port"
                class="w-full rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                type="number" placeholder="8080" />
            </div>

            <!-- Operation Mode -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Mode</label>
              <select
                v-model="config.targetMode"
                class="w-full rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500">
                <option value="connect">Connect</option>
                <option value="listen">Listen</option>
              </select>
            </div>

            <!-- Protocol -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Protocol</label>
              <select
                v-model="config.protocol"
                class="w-full rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500">
                <option value="TCP">TCP</option>
                <option value="UDP">UDP</option>
              </select>
            </div>

            <!-- NC Flavor -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Netcat Flavor</label>
              <select
                v-model="config.flavor"
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

        <!-- Network Options -->
        <div class="mb-4">
          <h3 class="text-xs font-medium text-gray-600 mb-2 uppercase tracking-wide">Network</h3>
          <div class="grid grid-cols-3 gap-2">
            <!-- Verbose -->
            <label class="flex items-center gap-2 p-2 rounded border border-gray-200 hover:bg-gray-50 cursor-pointer">
              <input
                v-model="config.isVerbose"
                class="size-3.5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                type="checkbox" />
              <div class="flex-1">
                <span class="text-xs font-medium text-gray-700">Verbose</span>
                <span class="ml-1 text-xs text-gray-400">(-v)</span>
              </div>
            </label>

            <!-- No DNS -->
            <label class="flex items-center gap-2 p-2 rounded border border-gray-200 hover:bg-gray-50 cursor-pointer">
              <input
                v-model="config.isNoDNS"
                class="size-3.5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                type="checkbox" />
              <div class="flex-1">
                <span class="text-xs font-medium text-gray-700">No DNS</span>
                <span class="ml-1 text-xs text-gray-400">(-n)</span>
              </div>
            </label>

            <!-- Keep Listening -->
            <label class="flex items-center gap-2 p-2 rounded border border-gray-200 hover:bg-gray-50 cursor-pointer">
              <input
                v-model="config.isKeepListening"
                class="size-3.5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                type="checkbox" />
              <div class="flex-1">
                <span class="text-xs font-medium text-gray-700">Keep Listening</span>
                <span class="ml-1 text-xs text-gray-400">(-k)</span>
              </div>
            </label>
          </div>
        </div>

        <!-- Advanced Options -->
        <div class="mb-4">
          <h3 class="text-xs font-medium text-gray-600 mb-2 uppercase tracking-wide">Advanced</h3>
          <div class="grid grid-cols-3 gap-2">
            <!-- Timeout -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Timeout</label>
              <div class="relative">
                <input
                  v-model.number="config.timeout"
                  class="w-full rounded border border-gray-300 px-2 py-1.5 pr-8 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  type="number" placeholder="5" />
                <span class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-gray-400">-w</span>
              </div>
            </div>

            <!-- Close Delay -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Close Delay</label>
              <div class="relative">
                <input
                  v-model.number="config.closeDelay"
                  class="w-full rounded border border-gray-300 px-2 py-1.5 pr-8 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  type="number" placeholder="0" />
                <span class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-gray-400">-q</span>
              </div>
            </div>

            <!-- Bind Script -->
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Bind Script</label>
              <div class="relative">
                <input
                  v-model="config.bindCommand"
                  class="w-full rounded border border-gray-300 px-2 py-1.5 pr-8 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  type="text" placeholder="shell command" />
                <span class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-gray-400">-s</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch, onMounted } from 'vue'
import { useProfileStore } from '../stores'
import type { Profile } from '../models'

const profileStore = useProfileStore()

// Create a reactive config object
const config = ref<Profile>({
  id: '',
  version: '1.0',
  profileName: '',
  host: 'localhost',
  port: 8080,
  targetMode: 'connect',
  protocol: 'TCP',
  flavor: 'GNU netcat',
  payloadMode: 'GET',
  outputType: 'printf',
  query: '',
  body: '',
  contentType: 'text/plain',
  connection: 'close',
  isVerbose: true,
  isNoDNS: false,
  isKeepListening: true,
  timeout: 5,
  closeDelay: 0,
  bindCommand: '',
})

// Load current profile on mount
onMounted(() => {
  loadCurrentProfile()
})

// Watch for profile changes from other components
watch(() => profileStore.currentProfile, () => {
  loadCurrentProfile()
}, { deep: true })

// Load the current profile into config
const loadCurrentProfile = () => {
  config.value = { ...profileStore.currentProfile }
}

// Watch config changes and update profile store
watch(config, (newConfig) => {
  profileStore.updateProfile(newConfig)
}, { deep: true })
</script>

<style></style>