import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { Profile, Folder } from "./models";

function createDefaultProfile(): Profile {
  return {
    id: crypto.randomUUID(),
    version: "1.0",
    profileName: "default",
    host: "localhost",
    port: 8080,
    path: "",
    targetMode: "connect",
    protocol: "TCP",
    flavor: "GNU netcat",
    payloadMode: "GET",
    outputType: "printf",
    query: "",
    body: "",
    rawPayload: "",
    contentType: "text/plain",
    connection: "close",
    isVerbose: true,
    isNoDNS: false,
    isKeepListening: true,
    timeout: 5,
    closeDelay: 0,
    bindCommand: "",
  };
}

export const useFolderStore = defineStore(
  "folder",
  () => {
    const generalFolderId = "-1";
    const folderDict = ref<Record<string, Folder>>({
      [generalFolderId]: {
        id: generalFolderId,
        folderName: "General",
        profiles: [
          {
            id: "default-profile",
            version: "1.0",
            profileName: "default",
            host: "localhost",
            port: 8080,
            path: "",
            targetMode: "connect",
            protocol: "TCP",
            flavor: "GNU netcat",
            payloadMode: "GET",
            outputType: "printf",
            query: "",
            body: "",
            rawPayload: "",
            contentType: "text/plain",
            connection: "close",
            isVerbose: true,
            isNoDNS: false,
            isKeepListening: true,
            timeout: 5,
            closeDelay: 0,
            bindCommand: "",
          },
        ],
      },
    });

    const addFolder = (folderName: string) => {
      // Check if folder name already exists
      const existingFolder = Object.values(folderDict.value).find(
        (f) => f.folderName === folderName,
      );
      if (existingFolder) {
        throw new Error(`Folder with name ${folderName} already exists.`);
      }

      const newFolder: Folder = {
        id: crypto.randomUUID(),
        folderName,
        profiles: [],
      };
      folderDict.value[newFolder.id] = newFolder;
      return newFolder;
    };

    const deleteFolder = (folderId: string) => {
      const folder = folderDict.value[folderId];
      if (!folder) {
        throw new Error(`Folder with id ${folderId} does not exist.`);
      }

      if (folder.folderName === "General") {
        throw new Error("General folder cannot be deleted.");
      }

      delete folderDict.value[folderId];
      return true;
    };

    const renameFolder = (folderId: string, newName: string) => {
      const folder = folderDict.value[folderId];
      if (!folder) {
        throw new Error(`Folder with id ${folderId} does not exist.`);
      }

      if (folder.folderName === "General") {
        throw new Error("General folder cannot be renamed.");
      }

      // Check if new name already exists
      const existingFolder = Object.values(folderDict.value).find(
        (f) => f.folderName === newName && f.id !== folderId,
      );
      if (existingFolder) {
        throw new Error(`Folder with name ${newName} already exists.`);
      }

      folder.folderName = newName;
      return true;
    };

    const addProfileToFolder = (folderId: string, profile: Profile) => {
      if (!folderDict.value[folderId]) {
        throw new Error(`Folder with id ${folderId} does not exist.`);
      }

      folderDict.value[folderId].profiles.push({ ...profile });
      return true;
    };

    const updateProfileInFolder = (folderId: string, profile: Profile) => {
      if (!folderDict.value[folderId]) {
        throw new Error(`Folder with id ${folderId} does not exist.`);
      }

      const index = folderDict.value[folderId].profiles.findIndex(
        (p) => p.id === profile.id,
      );

      if (index === -1) {
        throw new Error(
          `Profile with id ${profile.id} does not exist in folder ${folderId}.`,
        );
      }

      folderDict.value[folderId].profiles[index] = { ...profile };
      return true;
    };

    const deleteProfileFromFolder = (folderId: string, profileId: string) => {
      if (!folderDict.value[folderId]) {
        throw new Error(`Folder with id ${folderId} does not exist.`);
      }

      const profileIndex = folderDict.value[folderId].profiles.findIndex(
        (p) => p.id === profileId,
      );

      if (profileIndex === -1) {
        throw new Error(
          `Profile with id ${profileId} does not exist in folder ${folderId}.`,
        );
      }

      folderDict.value[folderId].profiles.splice(profileIndex, 1);
      return true;
    };

    const getFolderById = (folderId: string): Folder | undefined => {
      return folderDict.value[folderId];
    };

    const folderList = computed(() => {
      return Object.values(folderDict.value);
    });

    return {
      folderDict,
      addFolder,
      deleteFolder,
      renameFolder,
      addProfileToFolder,
      updateProfileInFolder,
      deleteProfileFromFolder,
      getFolderById,
      folderList,
    };
  },
  {
    persist: {
      key: "nc-folder-store-v2",
      storage: localStorage,
    },
  },
);

// user current profile store
export const useProfileStore = defineStore(
  "profile",
  () => {
    const currentProfile = ref<Profile>(createDefaultProfile());

    const resetProfile = () => {
      currentProfile.value = createDefaultProfile();
    };

    const loadProfile = (profile: Profile) => {
      currentProfile.value = { ...profile };
    };

    const updateProfile = (patch: Partial<Profile>) => {
      currentProfile.value = {
        ...currentProfile.value,
        ...patch,
      };
    };

    const outputCommand = computed(() => {
      // TODO : generate the full command base on the current profile
      return "nc command goes here";
      // const p = currentProfile.value;
      // const parts = ["nc"];
      // if (p.isVerbose) parts.push("-v");
      // if (p.isNoDNS) parts.push("-n");
      // if (p.isKeepListening) parts.push("-k");
      // if (p.timeout) parts.push(`-w ${p.timeout}`);
      // parts.push(p.host);
      // parts.push(String(p.port));
      // return parts.join(" ");
    });

    return {
      currentProfile,
      resetProfile,
      loadProfile,
      updateProfile,
      outputCommand,
    };
  },
  {
    persist: {
      key: "nc-current-profile-v2",
      storage: localStorage,
    },
  },
);
