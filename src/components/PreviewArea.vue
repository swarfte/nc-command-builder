<template>
  <div class="h-full flex flex-col bg-white">
    <div class="flex-1 overflow-y-auto p-2">
      <div class="w-full">
        <!-- <h2 class="text-lg font-semibold text-gray-800 mb-4">Command Preview</h2> -->

        <!-- Encoding Mode Selector -->
        <div class="mb-2">
          <div class="flex gap-2">
            <button v-for="mode in encodingModes" :key="mode.value" @click="encodingMode = mode.value" :class="[
              'px-4 py-2 text-sm rounded-md transition-colors',
              encodingMode === mode.value
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]">
              {{ mode.label }}
            </button>
          </div>
        </div>

        <!-- Generated Command -->
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-2">Netcat Command</label>
          <div class="relative">
            <pre
              class="w-full bg-gray-900 text-green-400 p-4 rounded-lg text-sm font-mono overflow-x-auto whitespace-pre-wrap">{{ generatedCommand }}</pre>
            <button @click="copyCommand"
              class="absolute top-2 right-2 px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white text-xs rounded">
              {{ copyButtonText }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useProfileStore } from '../stores'

const profileStore = useProfileStore()

// Encoding modes
const encodingModes = [
  { label: 'Original', value: 'original' },
  { label: 'URL-Encoded', value: 'url-encoded' },
]

const encodingMode = ref('original')
const copyButtonText = ref('Copy')

// Current configuration
const config = computed(() => profileStore.currentProfile)

// Generate the netcat command
const generatedCommand = computed(() => {
  return generateNetcatCommand()
})

// Generate netcat command based on configuration
const generateNetcatCommand = () => {
  const parts = []
  const cfg = config.value

  // Determine the base command based on flavor
  const baseCommand = getBaseCommand(cfg.flavor)
  parts.push(baseCommand)

  // Add protocol flag
  if (cfg.protocol === 'UDP') {
    const udpFlag = getUDPFlag(cfg.flavor)
    if (udpFlag) parts.push(udpFlag)
  }

  // Add listen mode if applicable
  if (cfg.targetMode === 'listen') {
    const listenFlag = getListenFlag(cfg.flavor)
    if (listenFlag) parts.push(listenFlag)
  }

  // Add verbose flag
  if (cfg.isVerbose) {
    parts.push('-v')
  }

  // Add no DNS flag
  if (cfg.isNoDNS) {
    parts.push('-n')
  }

  // Add keep listening flag
  if (cfg.isKeepListening) {
    const keepAliveFlag = getKeepAliveFlag(cfg.flavor)
    if (keepAliveFlag) parts.push(keepAliveFlag)
  }

  // Add timeout
  if (cfg.timeout) {
    parts.push(`-w ${cfg.timeout}`)
  }

  // Add close delay
  if (cfg.closeDelay) {
    parts.push(`-q ${cfg.closeDelay}`)
  }

  // Add bind script/address
  if (cfg.bindCommand) {
    parts.push(`-s ${cfg.bindCommand}`)
  }

  // Add host and port
  if (cfg.targetMode === 'connect') {
    parts.push(cfg.host)
    parts.push(cfg.port.toString())
  } else if (cfg.targetMode === 'listen') {
    // For listen mode, some flavors don't need host, others bind to specific host
    if (cfg.bindCommand) {
      parts.push(cfg.host) // Bind to specific host if using bind script
    }
    parts.push(cfg.port.toString())
  }

  // Add payload redirection for non-raw modes
  if (cfg.payloadMode !== 'Raw') {
    const payload = getPayloadForCommand()
    if (payload) {
      if (encodingMode.value === 'url-encoded') {
        parts.push(`<<< "${encodeURIComponent(payload)}"`)
      } else {
        parts.push(`<<< "${payload}"`)
      }
    }
  } else if (cfg.rawPayload) {
    // For raw mode, include the raw payload
    if (encodingMode.value === 'url-encoded') {
      parts.push(`<<< "${encodeURIComponent(cfg.rawPayload)}"`)
    } else {
      parts.push(`<<< "${cfg.rawPayload}"`)
    }
  }

  return parts.join(' ')
}

// Get base command for different netcat flavors
const getBaseCommand = (flavor: string) => {
  switch (flavor) {
    case 'GNU netcat':
      return 'nc'
    case 'OpenBSD netcat':
      return 'nc'
    case 'Netcat from FreeBSD':
      return 'nc'
    case 'Ncat (Nmap)':
      return 'ncat'
    case 'socat':
      return 'socat'
    default:
      return 'nc'
  }
}

// Get UDP flag for different flavors
const getUDPFlag = (flavor: string) => {
  switch (flavor) {
    case 'GNU netcat':
      return '-u'
    case 'OpenBSD netcat':
      return '-u'
    case 'Netcat from FreeBSD':
      return '-u'
    case 'Ncat (Nmap)':
      return '-u'
    case 'socat':
      return 'UDP' // socat uses different syntax
    default:
      return '-u'
  }
}

// Get listen flag for different flavors
const getListenFlag = (flavor: string) => {
  switch (flavor) {
    case 'GNU netcat':
      return '-l'
    case 'OpenBSD netcat':
      return '-l'
    case 'Netcat from FreeBSD':
      return '-l'
    case 'Ncat (Nmap)':
      return '-l'
    case 'socat':
      return null // socat uses different syntax
    default:
      return '-l'
  }
}

// Get keep-alive flag for different flavors
const getKeepAliveFlag = (flavor: string) => {
  switch (flavor) {
    case 'GNU netcat':
      return '-k'
    case 'OpenBSD netcat':
      return '-k'
    case 'Netcat from FreeBSD':
      return '-k'
    case 'Ncat (Nmap)':
      return '-k'
    case 'socat':
      return null // socat uses different syntax
    default:
      return '-k'
  }
}

// Get payload for command based on mode
const getPayloadForCommand = () => {
  const cfg = config.value

  if (cfg.payloadMode === 'GET') {
    return generateGETRequest()
  } else if (cfg.payloadMode === 'POST') {
    return generatePOSTRequest()
  }

  return ''
}

// Generate GET request
const generateGETRequest = () => {
  const cfg = config.value
  const queryParams = cfg.query || ''
  const path = cfg.path || '/'

  // Handle query parameters
  let fullPath = path
  if (queryParams) {
    fullPath += path.includes('?') ? `&${queryParams}` : `?${queryParams}`
  }

  let request = `GET ${fullPath} HTTP/1.1\r\n`
  request += `Host: ${cfg.host}\r\n`
  request += `User-Agent: netcat-command-builder\r\n`
  request += `Accept: */*\r\n`
  request += `Connection: ${cfg.connection}\r\n\r\n`

  return request
}

// Generate POST request
const generatePOSTRequest = () => {
  const cfg = config.value
  const path = cfg.path || '/'

  let request = `POST ${path} HTTP/1.1\r\n`
  request += `Host: ${cfg.host}\r\n`
  request += `User-Agent: netcat-command-builder\r\n`
  request += `Content-Type: ${cfg.contentType}\r\n`
  request += `Content-Length: ${cfg.body ? cfg.body.length : 0}\r\n`
  request += `Connection: ${cfg.connection}\r\n\r\n`

  if (cfg.body) {
    request += cfg.body
  }

  return request
}

// Copy command to clipboard
const copyCommand = async () => {
  try {
    await navigator.clipboard.writeText(generatedCommand.value)
    copyButtonText.value = 'Copied!'
    setTimeout(() => {
      copyButtonText.value = 'Copy'
    }, 2000)
  } catch (err) {
    copyButtonText.value = 'Failed'
    setTimeout(() => {
      copyButtonText.value = 'Copy'
    }, 2000)
  }
}
</script>

<style></style>