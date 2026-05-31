export interface Profile {
  id: string;
  version: string;
  profileName: string;
  host: string;
  port: number;
  path: string;
  targetMode: string;
  protocol: string;
  flavor: string;
  payloadMode: string;
  outputType: string;
  userAgent: string;
  cookie: string;
  query?: string;
  hiddenQuery?: string;
  body?: string;
  hiddenBody?: string;
  rawPayload?: string;
  hiddenCookie?: string;
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
