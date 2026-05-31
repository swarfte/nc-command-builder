<template>
  <div class="h-full flex flex-col bg-white">
    <div class="flex-1 overflow-y-auto pl-2 pr-2">
      <div class="w-full">


        <!-- Payload Mode Selector -->
        <div class="mb-2">
          <div class="flex gap-2">
            <button v-for="mode in payloadModes" :key="mode.value" @click="switchPayloadMode(mode.value)" :class="[
              'px-4 py-2 text-sm rounded-md transition-colors',
              activePanel === mode.value
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]">
              {{ mode.label }}
            </button>
          </div>
        </div>

        <!-- Raw Mode -->
        <div v-if="activePanel === 'Raw'" class="space-y-4">
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">Raw Payload</label>
            <textarea v-model="localConfig.rawPayload"
              class="w-full rounded border border-gray-300 px-3 py-2 text-sm font-mono focus:outline-none focus:ring-1 focus:ring-blue-500 min-h-[100px]"
              placeholder="Enter your raw payload here..." />
            <p class="mt-1 text-xs text-gray-500">Enter complete payload as you would send it via netcat</p>
          </div>
        </div>

        <!-- GET Mode -->
        <div v-if="activePanel === 'GET'" class="space-y-4">
          <div>
            <div class="grid grid-cols-12 gap-2 items-center mb-2">
              <label class="col-span-10 text-xs font-medium text-gray-600">Query Parameters</label>
              <button @click="addQueryParameter" type="button"
                class="col-span-2 inline-flex h-9 items-center justify-center gap-1.5 rounded-md border border-blue-200 bg-blue-50 px-2.5 text-xs font-medium text-blue-700 transition-colors hover:bg-blue-100 hover:text-blue-800">
                <span class="text-base leading-none">+</span>
                Add Parameter
              </button>
            </div>
            <div class="space-y-2">
              <div v-for="(param, index) in queryParameters" :key="index" class="grid grid-cols-12 gap-2 items-center">
                <input v-model="param.key" @input="debouncedUpdate"
                  class="col-span-5 h-9 rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  type="text" placeholder="Key" />
                <input v-model="param.value" @input="debouncedUpdate"
                  class="col-span-5 h-9 rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  type="text" placeholder="Value" />
                <button @click="removeQueryParameter(index)" type="button"
                  class="col-span-2 inline-flex h-9 items-center justify-center rounded-md border border-red-200 bg-red-50 px-2 text-xs font-medium text-red-600 transition-colors hover:bg-red-100 hover:text-red-700">
                  Remove
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- POST Mode -->
        <div v-if="activePanel === 'POST'" class="space-y-4">
          <!-- Content Type -->
          <div class="w-100">
            <label class="block text-xs font-medium text-gray-600 mb-1">Content Type</label>
            <select v-model="localConfig.contentType" @change="debouncedUpdate"
              class="w-full rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500">
              <option value="application/json">application/json</option>
              <option value="application/x-www-form-urlencoded">application/x-www-form-urlencoded</option>
              <option value="text/plain">text/plain</option>
              <option value="text/html">text/html</option>
              <option value="application/xml">application/xml</option>
            </select>
          </div>

          <!-- Body Parameters -->
          <div>
            <div class="grid grid-cols-12 gap-2 items-center mb-2">
              <label class="col-span-10 text-xs font-medium text-gray-600">Body Parameters</label>
              <button @click="addBodyParameter" type="button"
                class="col-span-2 inline-flex h-9 items-center justify-center gap-1.5 rounded-md border border-blue-200 bg-blue-50 px-2.5 text-xs font-medium text-blue-700 transition-colors hover:bg-blue-100 hover:text-blue-800">
                <span class="text-base leading-none">+</span>
                Add Parameter
              </button>
            </div>
            <div class="space-y-2">
              <div v-for="(param, index) in bodyParameters" :key="index" class="grid grid-cols-12 gap-2 items-center">
                <input v-model="param.key" @input="debouncedUpdate"
                  class="col-span-5 h-9 rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  type="text" placeholder="Key" />
                <input v-model="param.value" @input="debouncedUpdate"
                  class="col-span-5 h-9 rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  type="text" placeholder="Value" />
                <button @click="removeBodyParameter(index)" type="button"
                  class="col-span-2 inline-flex h-9 items-center justify-center rounded-md border border-red-200 bg-red-50 px-2 text-xs font-medium text-red-600 transition-colors hover:bg-red-100 hover:text-red-700">
                  Remove
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Cookie Mode -->
        <div v-if="activePanel === 'Cookie'" class="space-y-4">
          <div>
            <div class="grid grid-cols-12 gap-2 items-center mb-2">
              <label class="col-span-10 text-xs font-medium text-gray-600">Cookies</label>
              <button @click="addCookieParameter" type="button"
                class="col-span-2 inline-flex h-9 items-center justify-center gap-1.5 rounded-md border border-blue-200 bg-blue-50 px-2.5 text-xs font-medium text-blue-700 transition-colors hover:bg-blue-100 hover:text-blue-800">
                <span class="text-base leading-none">+</span>
                Add Cookie
              </button>
            </div>
            <div class="space-y-2">
              <div v-for="(cookie, index) in cookieParameters" :key="index"
                class="grid grid-cols-12 gap-2 items-center">
                <input v-model="cookie.key" @input="debouncedUpdate"
                  class="col-span-5 h-9 rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  type="text" placeholder="Name" />
                <input v-model="cookie.value" @input="debouncedUpdate"
                  class="col-span-5 h-9 rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  type="text" placeholder="Value" />
                <button @click="removeCookieParameter(index)" type="button"
                  class="col-span-2 inline-flex h-9 items-center justify-center rounded-md border border-red-200 bg-red-50 px-2 text-xs font-medium text-red-600 transition-colors hover:bg-red-100 hover:text-red-700">
                  Remove
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import { useProfileStore, useFolderStore } from '../stores'

const profileStore = useProfileStore()
const folderStore = useFolderStore()

// Track current profile ID to detect profile switches
const currentProfileId = ref('')
const isUpdatingFromStore = ref(false)
let updateTimeout: number | null = null

// Payload modes
const payloadModes = [
  { label: 'Raw', value: 'Raw' },
  { label: 'GET', value: 'GET' },
  { label: 'POST', value: 'POST' },
  { label: 'Cookie', value: 'Cookie' },
]

// Local config state
const localConfig = ref({
  payloadMode: 'GET',
  query: '',
  body: '',
  rawPayload: '',
  cookie: '',
  contentType: 'application/json',
})

const activePanel = ref<'Raw' | 'GET' | 'POST' | 'Cookie'>('GET')
const panelMemoryByProfile = ref<Record<string, typeof activePanel.value>>({})

// Query parameters for GET mode
const queryParameters = ref<Array<{ key: string; value: string }>>([])

// Body parameters for POST mode
const bodyParameters = ref<Array<{ key: string; value: string }>>([])

// Cookie parameters
const cookieParameters = ref<Array<{ key: string; value: string }>>([])

// Initialize 2 empty rows for parameters
const initializeEmptyParameters = (count: number = 2) => {
  return Array.from({ length: count }, () => ({ key: '', value: '' }))
}

// Load current profile into local config
const loadCurrentProfile = () => {
  const profile = profileStore.currentProfile

  // Check if this is actually a different profile
  if (profile.id === currentProfileId.value && isUpdatingFromStore.value) {
    return
  }

  isUpdatingFromStore.value = true
  currentProfileId.value = profile.id

  localConfig.value = {
    payloadMode: profile.payloadMode || 'GET',
    query: profile.query || '',
    body: profile.body || '',
    rawPayload: profile.rawPayload || '',
    cookie: profile.cookie || '',
    contentType: profile.contentType || 'application/json',
  }

  activePanel.value = panelMemoryByProfile.value[profile.id]
    ?? ((profile.payloadMode as typeof activePanel.value) || 'GET')

  // Parse query parameters from query string
  if (profile.query) {
    const parsed = profile.query.split('&')
      .filter(param => param.includes('='))
      .map(param => {
        const [key, value] = param.split('=')
        return { key: decodeURIComponent(key), value: decodeURIComponent(value) }
      })
    queryParameters.value = parsed.length > 0 ? parsed : initializeEmptyParameters()
  } else {
    queryParameters.value = initializeEmptyParameters()
  }

  // Parse body parameters from body string
  if (profile.body && profile.contentType === 'application/json') {
    try {
      const obj = JSON.parse(profile.body)
      const parsed = Object.entries(obj)
        .map(([key, value]) => ({ key, value: String(value) }))
      bodyParameters.value = parsed.length > 0 ? parsed : initializeEmptyParameters()
    } catch {
      bodyParameters.value = initializeEmptyParameters()
    }
  } else if (profile.body && profile.contentType === 'application/x-www-form-urlencoded') {
    const parsed = profile.body.split('&')
      .filter(param => param.includes('='))
      .map(param => {
        const [key, value] = param.split('=')
        return { key: decodeURIComponent(key), value: decodeURIComponent(value) }
      })
    bodyParameters.value = parsed.length > 0 ? parsed : initializeEmptyParameters()
  } else {
    bodyParameters.value = initializeEmptyParameters()
  }

  // Parse cookie parameters from cookie string
  if (profile.cookie) {
    const parsed = profile.cookie.split(';')
      .map(part => part.trim())
      .filter(part => part.includes('='))
      .map(part => {
        const [key, ...valueParts] = part.split('=')
        return { key: key.trim(), value: valueParts.join('=').trim() }
      })
    cookieParameters.value = parsed.length > 0 ? parsed : initializeEmptyParameters()
  } else {
    cookieParameters.value = initializeEmptyParameters()
  }

  // Reset flag after a small delay
  setTimeout(() => {
    isUpdatingFromStore.value = false
  }, 100)
}

// Find the folder that contains the current profile
const findFolderForProfile = (profileId: string) => {
  return folderStore.folderList.find(folder =>
    folder.profiles.some(profile => profile.id === profileId)
  )
}

// Update profile in both stores
const updateProfileInStores = () => {
  if (isUpdatingFromStore.value) return

  localConfig.value.cookie = cookieParameters.value
    .filter(p => p.key && p.value)
    .map(p => `${p.key}=${p.value}`)
    .join('; ')

  // Build query string from parameters for GET mode
  if (localConfig.value.payloadMode === 'GET') {
    localConfig.value.query = queryParameters.value
      .filter(p => p.key && p.value)
      .map(p => `${encodeURIComponent(p.key)}=${encodeURIComponent(p.value)}`)
      .join('&')
    localConfig.value.body = ''
    localConfig.value.rawPayload = ''
  }

  // Build body string from parameters for POST mode
  if (localConfig.value.payloadMode === 'POST') {
    if (localConfig.value.contentType === 'application/json') {
      const obj = bodyParameters.value
        .filter(p => p.key && p.value)
        .reduce((acc, p) => ({ ...acc, [p.key]: p.value }), {})
      localConfig.value.body = JSON.stringify(obj)
    } else if (localConfig.value.contentType === 'application/x-www-form-urlencoded') {
      localConfig.value.body = bodyParameters.value
        .filter(p => p.key && p.value)
        .map(p => `${encodeURIComponent(p.key)}=${encodeURIComponent(p.value)}`)
        .join('&')
    } else {
      localConfig.value.body = bodyParameters.value
        .filter(p => p.key && p.value)
        .map(p => `${p.key}: ${p.value}`)
        .join('\n')
    }
    localConfig.value.query = ''
    localConfig.value.rawPayload = ''
  }

  // For Raw mode, use rawPayload directly
  if (localConfig.value.payloadMode === 'Raw') {
    localConfig.value.query = ''
    localConfig.value.body = ''
  }

  // Update current profile in profile store
  isUpdatingFromStore.value = true
  profileStore.updateProfile({
    payloadMode: localConfig.value.payloadMode,
    query: localConfig.value.query,
    body: localConfig.value.body,
    rawPayload: localConfig.value.rawPayload,
    cookie: localConfig.value.cookie,
    contentType: localConfig.value.contentType,
  })

  // Also update the profile in the folder store
  const folder = findFolderForProfile(currentProfileId.value)
  if (folder) {
    const updatedProfile = {
      ...profileStore.currentProfile,
      payloadMode: localConfig.value.payloadMode,
      query: localConfig.value.query,
      body: localConfig.value.body,
      rawPayload: localConfig.value.rawPayload,
      cookie: localConfig.value.cookie,
      contentType: localConfig.value.contentType,
    }
    folderStore.updateProfileInFolder(folder.id, updatedProfile)
  }

  // Reset flag
  setTimeout(() => {
    isUpdatingFromStore.value = false
  }, 50)
}

// Debounced update for input changes
const debouncedUpdate = () => {
  if (updateTimeout) clearTimeout(updateTimeout)
  updateTimeout = setTimeout(() => {
    updateProfileInStores()
  }, 300) as unknown as number
}

// Switch payload mode
const switchPayloadMode = (mode: string) => {
  if (mode === 'Cookie') {
    activePanel.value = 'Cookie'
    panelMemoryByProfile.value[currentProfileId.value] = 'Cookie'
    return
  }

  activePanel.value = mode as typeof activePanel.value
  panelMemoryByProfile.value[currentProfileId.value] = activePanel.value
  localConfig.value.payloadMode = mode
  updateProfileInStores()
}

// Add query parameter
const addQueryParameter = () => {
  queryParameters.value.push({ key: '', value: '' })
  nextTick(() => {
    updateProfileInStores()
  })
}

// Remove query parameter
const removeQueryParameter = (index: number) => {
  queryParameters.value.splice(index, 1)
  nextTick(() => {
    updateProfileInStores()
  })
}

// Add body parameter
const addBodyParameter = () => {
  bodyParameters.value.push({ key: '', value: '' })
  nextTick(() => {
    updateProfileInStores()
  })
}

// Remove body parameter
const removeBodyParameter = (index: number) => {
  bodyParameters.value.splice(index, 1)
  nextTick(() => {
    updateProfileInStores()
  })
}

// Add cookie parameter
const addCookieParameter = () => {
  cookieParameters.value.push({ key: '', value: '' })
  nextTick(() => {
    updateProfileInStores()
  })
}

// Remove cookie parameter
const removeCookieParameter = (index: number) => {
  cookieParameters.value.splice(index, 1)
  nextTick(() => {
    updateProfileInStores()
  })
}

// Watch for profile ID changes (profile switching)
watch(() => profileStore.currentProfile.id, (newId, oldId) => {
  if (newId !== oldId) {
    loadCurrentProfile()
  }
})

// Watch local config changes (for raw payload and content type)
watch(localConfig, () => {
  if (!isUpdatingFromStore.value) {
    updateProfileInStores()
  }
}, { deep: true })

// Load current profile on mount
onMounted(() => {
  loadCurrentProfile()
})
</script>

<style></style>