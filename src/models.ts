export interface Profile {
  folderName: string;
  profileName: string;
  host: string;
  port: number;
  targetMode: string;
  protocol: string;
  flavor: string;
  payloadMode: string;
  outputType: string;
  outputCommand: string;
  query?: string;
  body?: string;
  contentType: string;
  contentLength: number;
  connection: string;
  isVerbose: boolean;
  isNoDNS: boolean;
  isKeepListening: boolean;
  timeout: number;
  closeDelay?: number;
  bindCommand?: string;
}

export interface Folder {
  folderName: string;
  profiles: Profile[];
}
