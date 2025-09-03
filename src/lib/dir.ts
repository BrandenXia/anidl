import path from "path";
import os from "os";

export const appDir = () => path.resolve(os.homedir(), ".anidl");
