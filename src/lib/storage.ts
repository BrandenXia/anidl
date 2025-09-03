import path from "path";

import { appDir } from "./dir";
import { createKeyv } from "@keyv/sqlite";
import type Keyv from "keyv";

const dbPath = () => path.resolve(appDir(), "db.sqlite");

export const cache: Keyv<string> = createKeyv({
  db: `sqlite://${dbPath()}`,
  table: "cache",
  busyTimeout: 10000,
});
