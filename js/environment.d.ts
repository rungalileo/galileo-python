declare global {
  namespace NodeJS {
    interface ProcessEnv {
      GALILEO_CONSOLE_URL?: string;
      GALILEO_API_KEY?: string;
    }
  }
}

export {};
