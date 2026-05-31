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
                <input v-model="param.enabled" @change="debouncedUpdate"
                  class="col-span-1 h-9 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  type="checkbox" />
                <input v-model="param.key" @input="debouncedUpdate"
                  class="col-span-3 h-9 rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  type="text" placeholder="Key" />
                <input v-model="param.value" @input="debouncedUpdate"
                  class="col-span-6 h-9 rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
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
                <input v-model="param.enabled" @change="debouncedUpdate"
                  class="col-span-1 h-9 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  type="checkbox" />
                <input v-model="param.key" @input="debouncedUpdate"
                  class="col-span-5 h-9 rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  type="text" placeholder="Key" />
                <input v-model="param.value" @input="debouncedUpdate"
                  class="col-span-4 h-9 rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
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
                <input v-model="cookie.enabled" @change="debouncedUpdate"
                  class="col-span-1 h-9 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  type="checkbox" />
                <input v-model="cookie.key" @input="debouncedUpdate"
                  class="col-span-5 h-9 rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  type="text" placeholder="Name" />
                <input v-model="cookie.value" @input="debouncedUpdate"
                  class="col-span-4 h-9 rounded border border-gray-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
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
  hiddenQuery: '',
  body: '',
  hiddenBody: '',
  rawPayload: '',
  cookie: '',
  hiddenCookie: '',
  contentType: 'application/json',
})

const activePanel = ref<'Raw' | 'GET' | 'POST' | 'Cookie'>('GET')
const panelMemoryByProfile = ref<Record<string, typeof activePanel.value>>({})

// Query parameters for GET mode
const queryParameters = ref<Array<{ key: string; value: string; enabled: boolean }>>([])

// Body parameters for POST mode
const bodyParameters = ref<Array<{ key: string; value: string; enabled: boolean }>>([])

// Cookie parameters
const cookieParameters = ref<Array<{ key: string; value: string; enabled: boolean }>>([])

// Initialize 2 empty rows for parameters
const initializeEmptyParameters = (count: number = 2) => {
  return Array.from({ length: count }, () => ({ key: '', value: '', enabled: true }))
}

const parseFormLikeString = (input: string) => {
  return input.split('&')
    .filter(param => param.includes('='))
    .map(param => {
      const [key, value] = param.split('=')
      return { key: decodeURIComponent(key), value: decodeURIComponent(value) }
    })
}

const parseTextPairs = (input: string) => {
  return input.split('\n')
    .map(line => line.trim())
    .filter(line => line.includes(':'))
    .map(line => {
      const [key, ...valueParts] = line.split(':')
      return { key: key.trim(), value: valueParts.join(':').trim() }
    })
}

const parseCookieString = (input: string) => {
  return input.split(';')
    .map(part => part.trim())
    .filter(part => part.includes('='))
    .map(part => {
      const [key, ...valueParts] = part.split('=')
      return { key: key.trim(), value: valueParts.join('=').trim() }
    })
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
    hiddenQuery: profile.hiddenQuery || '',
    body: profile.body || '',
    hiddenBody: profile.hiddenBody || '',
    rawPayload: profile.rawPayload || '',
    cookie: profile.cookie || '',
    hiddenCookie: profile.hiddenCookie || '',
    contentType: profile.contentType || 'application/json',
  }

  activePanel.value = panelMemoryByProfile.value[profile.id]
    ?? ((profile.payloadMode as typeof activePanel.value) || 'GET')

  // Parse query parameters from query string
  const enabledQuery = profile.query ? parseFormLikeString(profile.query) : []
  const hiddenQuery = profile.hiddenQuery ? parseFormLikeString(profile.hiddenQuery) : []
  queryParameters.value = [
    ...enabledQuery.map(param => ({ ...param, enabled: true })),
    ...hiddenQuery.map(param => ({ ...param, enabled: false })),
  ]
  if (queryParameters.value.length === 0) {
    queryParameters.value = initializeEmptyParameters()
  }

  // Parse body parameters from body string
  const contentType = profile.contentType || 'application/json'
  let enabledBody: Array<{ key: string; value: string }> = []
  let hiddenBody: Array<{ key: string; value: string }> = []

  if (contentType === 'application/json') {
    try {
      if (profile.body) {
        const obj = JSON.parse(profile.body)
        enabledBody = Object.entries(obj).map(([key, value]) => ({ key, value: String(value) }))
      }
    } catch {
      enabledBody = []
    }
    try {
      if (profile.hiddenBody) {
        const obj = JSON.parse(profile.hiddenBody)
        hiddenBody = Object.entries(obj).map(([key, value]) => ({ key, value: String(value) }))
      }
    } catch {
      hiddenBody = []
    }
  } else if (contentType === 'application/x-www-form-urlencoded') {
    enabledBody = profile.body ? parseFormLikeString(profile.body) : []
    hiddenBody = profile.hiddenBody ? parseFormLikeString(profile.hiddenBody) : []
  } else {
    enabledBody = profile.body ? parseTextPairs(profile.body) : []
    hiddenBody = profile.hiddenBody ? parseTextPairs(profile.hiddenBody) : []
  }

  bodyParameters.value = [
    ...enabledBody.map(param => ({ ...param, enabled: true })),
    ...hiddenBody.map(param => ({ ...param, enabled: false })),
  ]
  if (bodyParameters.value.length === 0) {
    bodyParameters.value = initializeEmptyParameters()
  }

  // Parse cookie parameters from cookie string
  const enabledCookies = profile.cookie ? parseCookieString(profile.cookie) : []
  const hiddenCookies = profile.hiddenCookie ? parseCookieString(profile.hiddenCookie) : []
  cookieParameters.value = [
    ...enabledCookies.map(param => ({ ...param, enabled: true })),
    ...hiddenCookies.map(param => ({ ...param, enabled: false })),
  ]
  if (cookieParameters.value.length === 0) {
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

  const enabledCookies = cookieParameters.value.filter(p => p.enabled)
  const hiddenCookies = cookieParameters.value.filter(p => !p.enabled)

  localConfig.value.cookie = enabledCookies
    .filter(p => p.key && p.value)
    .map(p => `${p.key}=${p.value}`)
    .join('; ')
  localConfig.value.hiddenCookie = hiddenCookies
    .filter(p => p.key && p.value)
    .map(p => `${p.key}=${p.value}`)
    .join('; ')

  // Build query string from parameters for GET mode
  const enabledQuery = queryParameters.value.filter(p => p.enabled)
  const hiddenQuery = queryParameters.value.filter(p => !p.enabled)
  const enabledQueryString = enabledQuery
    .filter(p => p.key && p.value)
    .map(p => `${encodeURIComponent(p.key)}=${encodeURIComponent(p.value)}`)
    .join('&')
  const hiddenQueryString = hiddenQuery
    .filter(p => p.key && p.value)
    .map(p => `${encodeURIComponent(p.key)}=${encodeURIComponent(p.value)}`)
    .join('&')

  if (localConfig.value.payloadMode === 'GET') {
    localConfig.value.query = enabledQueryString
    localConfig.value.body = ''
    localConfig.value.rawPayload = ''
  } else {
    localConfig.value.query = ''
  }
  localConfig.value.hiddenQuery = hiddenQueryString

  // Build body string from parameters for POST mode
  const enabledBody = bodyParameters.value.filter(p => p.enabled)
  const hiddenBody = bodyParameters.value.filter(p => !p.enabled)

  const buildBodyString = (params: Array<{ key: string; value: string }>) => {
    const filtered = params.filter(p => p.key && p.value)
    if (filtered.length === 0) return ''

    if (localConfig.value.contentType === 'application/json') {
      const obj = filtered.reduce((acc, p) => ({ ...acc, [p.key]: p.value }), {})
      return JSON.stringify(obj)
    }
    if (localConfig.value.contentType === 'application/x-www-form-urlencoded') {
      return filtered
        .map(p => `${encodeURIComponent(p.key)}=${encodeURIComponent(p.value)}`)
        .join('&')
    }
    return filtered.map(p => `${p.key}: ${p.value}`).join('\n')
  }

  const enabledBodyString = buildBodyString(enabledBody)
  const hiddenBodyString = buildBodyString(hiddenBody)

  if (localConfig.value.payloadMode === 'POST') {
    localConfig.value.body = enabledBodyString
    localConfig.value.query = ''
    localConfig.value.rawPayload = ''
  } else {
    localConfig.value.body = ''
  }
  localConfig.value.hiddenBody = hiddenBodyString

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
    hiddenQuery: localConfig.value.hiddenQuery,
    body: localConfig.value.body,
    hiddenBody: localConfig.value.hiddenBody,
    rawPayload: localConfig.value.rawPayload,
    cookie: localConfig.value.cookie,
    hiddenCookie: localConfig.value.hiddenCookie,
    contentType: localConfig.value.contentType,
  })

  // Also update the profile in the folder store
  const folder = findFolderForProfile(currentProfileId.value)
  if (folder) {
    const updatedProfile = {
      ...profileStore.currentProfile,
      payloadMode: localConfig.value.payloadMode,
      query: localConfig.value.query,
      hiddenQuery: localConfig.value.hiddenQuery,
      body: localConfig.value.body,
      hiddenBody: localConfig.value.hiddenBody,
      rawPayload: localConfig.value.rawPayload,
      cookie: localConfig.value.cookie,
      hiddenCookie: localConfig.value.hiddenCookie,
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
  queryParameters.value.push({ key: '', value: '', enabled: true })
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
  bodyParameters.value.push({ key: '', value: '', enabled: true })
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
  cookieParameters.value.push({ key: '', value: '', enabled: true })
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