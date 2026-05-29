import { defineStore } from "pinia";
import { ref } from "vue";
import type { Profile, Folder } from "./models";

export const useFolderStore = defineStore(
  "folder",
  () => {
    const folderDict = ref<Record<string, Folder>>({
      General: {
        folderName: "General",
        profiles: [],
      },
    });

    const addFolder = (folderName: string) => {
      if (folderDict.value[folderName]) {
        throw new Error(`Folder with name ${folderName} already exists.`);
      }
      folderDict.value[folderName] = {
        folderName,
        profiles: [],
      };
      return true;
    };

    const deleteFolder = (folderName: string) => {
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
      folderDict.value[folderName].profiles.push(profile);
      return true;
    };

    const deleteProfileFromFolder = (
      folderName: string,
      profileName: string,
    ) => {
      if (!folderDict.value[folderName]) {
        throw new Error(`Folder with name ${folderName} does not exist.`);
      }
      const profileIndex = folderDict.value[folderName].profiles.findIndex(
        (p) => p.profileName === profileName,
      );
      if (profileIndex === -1) {
        throw new Error(
          `Profile with name ${profileName} does not exist in folder ${folderName}.`,
        );
      }
      folderDict.value[folderName].profiles.splice(profileIndex, 1);
      return true;
    };

    return {
      folderDict,
      addFolder,
      deleteFolder,
      addProfileToFolder,
      deleteProfileFromFolder,
    };
  },
  {
    persist: {
      storage: localStorage,
    },
  },
);

// user current profile store
export const useProfileStore = defineStore(
  "profile",
  () => {
    const profileName = ref<string>("default");
    const folderName = ref<string>("General");
    const host = ref<string>("localhost");
    const port = ref<number>(8080);
    const targetMode = ref<string>("connect");
    const protocol = ref<string>("TCP");
    const flavor = ref<string>("GNU netcat");
    const payloadMode = ref<string>("GET");
    const outputType = ref<string>("printf");
    const outputCommand = ref<string>("");
    const query = ref<string>("");
    const body = ref<string>("");
    const contentType = ref<string>("text/plain");
    const contentLength = ref<number>(0);
    const connection = ref<string>("close");
    const isVerbose = ref<boolean>(true);
    const isNoDNS = ref<boolean>(false);
    const isKeepListening = ref<boolean>(true);
    const timeout = ref<number>(5);
    const closeDelay = ref<number>(0);
    const bindCommand = ref<string>("");

    return {
      profileName,
      folderName,
      host,
      port,
      targetMode,
      protocol,
      flavor,
      payloadMode,
      outputType,
      outputCommand,
      query,
      body,
      contentType,
      contentLength,
      connection,
      isVerbose,
      isNoDNS,
      isKeepListening,
      timeout,
      closeDelay,
      bindCommand,
    };
  },
  {
    persist: {
      storage: localStorage,
    },
  },
);
