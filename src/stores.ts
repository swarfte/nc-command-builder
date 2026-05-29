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
    targetMode: "connect",
    protocol: "TCP",
    flavor: "GNU netcat",
    payloadMode: "GET",
    outputType: "printf",
    query: "",
    body: "",
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
    const folderDict = ref<Record<string, Folder>>({
      General: {
        id: crypto.randomUUID(),
        folderName: "General",
        profiles: [],
      },
    });

    const addFolder = (folderName: string) => {
      if (folderDict.value[folderName]) {
        throw new Error(`Folder with name ${folderName} already exists.`);
      }
      folderDict.value[folderName] = {
        id: crypto.randomUUID(),
        folderName,
        profiles: [],
      };
      return true;
    };

    const deleteFolder = (folderName: string) => {
      if (folderName === "General") {
        throw new Error("General folder cannot be deleted.");
      }

      if (!folderDict.value[folderName]) {
        throw new Error(`Folder with name ${folderName} does not exist.`);
      }
      delete folderDict.value[folderName];
      return true;
    };

    const addProfileToFolder = (folderName: string, profile: Profile) => {
      if (!folderDict.value[folderName]) {
        throw new Error(`Folder with name ${folderName} does not exist.`);
      }

      folderDict.value[folderName].profiles.push(structuredClone(profile));
      return true;
    };

    const updateProfileInFolder = (folderName: string, profile: Profile) => {
      if (!folderDict.value[folderName]) {
        throw new Error(`Folder with name ${folderName} does not exist.`);
      }

      const index = folderDict.value[folderName].profiles.findIndex(
        (p) => p.id === profile.id,
      );

      if (index === -1) {
        throw new Error(
          `Profile with id ${profile.id} does not exist in folder ${folderName}.`,
        );
      }

      folderDict.value[folderName].profiles[index] = structuredClone(profile);
      return true;
    };

    const deleteProfileFromFolder = (folderName: string, profileId: string) => {
      if (!folderDict.value[folderName]) {
        throw new Error(`Folder with name ${folderName} does not exist.`);
      }

      const profileIndex = folderDict.value[folderName].profiles.findIndex(
        (p) => p.id === profileId,
      );

      if (profileIndex === -1) {
        throw new Error(
          `Profile with id ${profileId} does not exist in folder ${folderName}.`,
        );
      }

      folderDict.value[folderName].profiles.splice(profileIndex, 1);
      return true;
    };

    const folderList = computed(() => {
      return Object.values(folderDict.value);
    });

    return {
      folderDict,
      addFolder,
      deleteFolder,
      addProfileToFolder,
      updateProfileInFolder,
      deleteProfileFromFolder,
      folderList,
    };
  },
  {
    persist: {
      key: "nc-folder-store-v1",
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
      currentProfile.value = structuredClone(profile);
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
      key: "nc-current-profile-v1",
      storage: localStorage,
    },
  },
);
