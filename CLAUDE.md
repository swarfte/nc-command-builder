# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Vue.js + TypeScript web application** that provides a GUI for building netcat commands. The application is designed for CTF players, pentesters, and security professionals who need to quickly construct complex netcat commands with proper payloads.

**Note:** The README.md references a Python/Tkinter version that appears to be from an earlier iteration or different implementation. The current codebase is entirely Vue.js + TypeScript.

## Development Commands

### Running the Development Server
```bash
npm run dev
```
Starts the Vite development server with hot reload.

### Building for Production
```bash
npm run build
```
Builds the application using `vue-tsc` for type checking followed by `vite build`. Output is in the `dist/` directory.

### Preview Production Build
```bash
npm run preview
```
Preview the production build locally.

## Architecture

### State Management with Pinia

The application uses **Pinia** for state management with two primary stores that sync with each other:

1. **useFolderStore** (`src/stores.ts` lines 32-196)
   - Manages profile organization in folders
   - Persists to localStorage as `nc-folder-store-v2`
   - Contains folder CRUD operations and profile storage
   - Includes a "General" folder that cannot be deleted

2. **useProfileStore** (`src/stores.ts` lines 199-247)
   - Manages the currently active profile
   - Persists to localStorage as `nc-current-profile-v2`
   - Provides `updateProfile()`, `loadProfile()`, and `resetProfile()` methods

**Important:** When updating profile data, you typically need to update **both stores** to keep them synchronized. See the pattern in `ConfigArea.vue` lines 208-226.

### Component Architecture

The application uses a **4-panel grid layout** (`src/App.vue`):

1. **ProfileArea** (`src/components/ProfileArea.vue`)
   - Left sidebar for profile management
   - Folder organization with create/rename/delete
   - Profile save/load functionality
   - Tree-view navigation

2. **ConfigArea** (`src/components/ConfigArea.vue`)
   - Target configuration (host, port, path)
   - Connection settings (mode, protocol, netcat flavor)
   - Advanced options (timeout, DNS, verbose, keep-alive)
   - Uses local state with two-way binding to stores

3. **PayloadArea** (`src/components/PayloadArea.vue`)
   - Three payload modes: Raw, GET, POST
   - **Raw mode**: Direct text input for custom payloads
   - **GET mode**: Key-value parameter builder for query strings
   - **POST mode**: Key-value body parameter builder with content-type selection
   - Each mode maintains independent data that's preserved when switching

4. **PreviewArea** (`src/components/PreviewArea.vue`)
   - Real-time command generation and preview
   - Flavor-specific flag handling (GNU vs OpenBSD vs Ncat vs socat)
   - Copy-to-clipboard functionality
   - Contains the core command generation logic

### Data Flow Patterns

**Profile Updates:**
```
User Input → Component Local State → useProfileStore.updateProfile() → useFolderStore.updateProfileInFolder()
```

**Mode Switching:**
When switching between payload modes (Raw/GET/POST), each mode maintains its own independent data. The component tracks the current profile ID to detect profile switches and reload data appropriately.

**Command Generation:**
The `PreviewArea` component contains `generateNetcatCommand()` (lines 42-117) which:
1. Selects appropriate base command and flags based on netcat flavor
2. Handles flavor-specific syntax differences
3. Generates HTTP requests for GET/POST modes with proper headers
4. Applies URL encoding when needed

### Key TypeScript Types

**Profile Interface** (`src/models.ts` lines 1-24):
```typescript
interface Profile {
  id: string;                    // UUID identifier
  version: string;               // Schema version
  profileName: string;          // Display name
  host: string;                 // Target hostname
  port: number;                 // Target port
  path: string;                 // HTTP path
  targetMode: string;           // 'connect' | 'listen'
  protocol: string;             // 'TCP' | 'UDP'
  flavor: string;               // Netcat flavor
  payloadMode: string;          // 'Raw' | 'GET' | 'POST'
  outputType: string;           // 'printf' | 'echo'
  query?: string;               // GET query string
  body?: string;                // POST body content
  rawPayload?: string;          // Raw payload text
  contentType: string;         // HTTP content type
  connection: string;           // HTTP connection header
  // ... various boolean flags and numeric options
}
```

**Folder Interface** (`src/models.ts` lines 26-30):
```typescript
interface Folder {
  id: string;
  folderName: string;
  profiles: Profile[];
}
```

## Common Development Patterns

### Adding New Configuration Options
1. Add the field to the `Profile` interface in `src/models.ts`
2. Update `createDefaultProfile()` in `src/stores.ts`
3. Add UI controls in the appropriate component (typically `ConfigArea.vue`)
4. Include the field in command generation logic in `PreviewArea.vue`

### Adding Netcat Flavors
Update the flavor-specific functions in `PreviewArea.vue`:
- `getBaseCommand()` (lines 120-135)
- `getUDPFlag()` (lines 138-153)
- `getListenFlag()` (lines 156-172)
- `getKeepAliveFlag()` (lines 174-189)

### Component Communication
Components use Pinia stores for shared state. When a component needs to react to profile changes from elsewhere, use the `watch()` pattern:
```typescript
watch(() => profileStore.currentProfile.id, (newId, oldId) => {
  if (newId !== oldId) {
    loadCurrentProfile()
  }
})
```

## Technology Stack

- **Vue 3** with Composition API and `<script setup>`
- **TypeScript** for type safety
- **Vite** as build tool and dev server
- **Pinia** for state management with persistence
- **Tailwind CSS v4** for styling
- **Vue DevTools** plugin for debugging

## File Structure

```
src/
├── App.vue              # Main layout with 4-panel grid
├── main.ts              # Application entry point
├── models.ts            # TypeScript interfaces (Profile, Folder)
├── stores.ts            # Pinia stores (useFolderStore, useProfileStore)
├── style.css            # Global styles
└── components/
    ├── ConfigArea.vue   # Target and connection configuration
    ├── PayloadArea.vue  # Payload editor (Raw/GET/POST modes)
    ├── PreviewArea.vue  # Command generation and preview
    └── ProfileArea.vue  # Profile management sidebar
```