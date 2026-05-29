export interface Profile {
  id: string;
  version: string;
  profileName: string;
  host: string;
  port: number;
  targetMode: string;
  protocol: string;
  flavor: string;
  payloadMode: string;
  outputType: string;
  query?: string;
  body?: string;
  contentType: string;
  connection: string;
  isVerbose: boolean;
  isNoDNS: boolean;
  isKeepListening: boolean;
  timeout: number;
  closeDelay?: number;
  bindCommand?: string;
}

export interface Folder {
  id: string;
  folderName: string;
  profiles: Profile[];
}
