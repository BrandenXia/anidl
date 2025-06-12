import tomllib
from pathlib import Path
from typing import Literal, TypedDict, cast

import tomli_w

CONFIG_DIR = Path.home() / ".config" / "anidl"
CONFIG_FILE = CONFIG_DIR / "config.toml"


class ConfigDict(TypedDict):
    anime_dir: str


type ConfigDictKeys = Literal["anime_dir"]


DEFAULT_CONFIG: ConfigDict = {"anime_dir": ""}


class Config:
    _instance = None
    __slots__ = ("config", *DEFAULT_CONFIG.keys())

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not CONFIG_DIR.exists():
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        self.config: ConfigDict
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "rb") as f:
                self.config = cast(ConfigDict, DEFAULT_CONFIG | tomllib.load(f))
        else:
            self.config = DEFAULT_CONFIG

    def save(self):
        with open(CONFIG_FILE, "wb") as f:
            tomli_w.dump(self.config, f)

    def __getattr__(self, key: str) -> str:
        if key not in self.config:
            raise AttributeError(f"Config has no attribute '{key}'")

        return self.config[cast(ConfigDictKeys, key)]

    def __setattr__(self, key: str, value: str):
        if key == "config":
            super().__setattr__(key, value)
            return

        if key not in self.config:
            raise AttributeError(f"Config has no attribute '{key}'")

        self.config[cast(ConfigDictKeys, key)] = value
        self.save()

    def get_anime_dir(self) -> Path:
        return Path(self.anime_dir).expanduser()
