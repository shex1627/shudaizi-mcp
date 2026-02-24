"""Configuration manager for loading and querying JSON config files."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class ConfigError(Exception):
    """Raised for any configuration problem."""
    pass


class ConfigManager:
    """Loads and provides access to application configuration."""

    def __init__(self, config_path: str):
        self._path = Path(config_path)
        self._data: dict = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            raise ConfigError(f"Config file not found: {self._path}")
        with open(self._path) as f:
            self._data = json.load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a config value by dot-separated key path."""
        if not key:
            raise ConfigError("Key cannot be empty")
        if not isinstance(key, str):
            raise ConfigError(f"Key must be a string, got {type(key).__name__}")

        parts = key.split(".")
        current = self._data
        for part in parts:
            if not isinstance(current, dict):
                raise ConfigError(f"Cannot traverse into non-dict at '{part}' in key '{key}'")
            if part not in current:
                if default is not None:
                    return default
                raise ConfigError(f"Key '{key}' not found in config and no default provided")
            current = current[part]
        return current

    def get_int(self, key: str, default: int | None = None) -> int:
        """Get a config value as integer."""
        value = self.get(key, default)
        if value is None:
            raise ConfigError(f"Key '{key}' not found and no default provided")
        if isinstance(value, bool):
            raise ConfigError(f"Key '{key}' is a boolean, not an integer")
        if not isinstance(value, (int, float, str)):
            raise ConfigError(f"Key '{key}' has type {type(value).__name__}, cannot convert to int")
        try:
            return int(value)
        except (ValueError, TypeError):
            raise ConfigError(f"Cannot convert '{value}' to int for key '{key}'")

    def get_str(self, key: str, default: str | None = None) -> str:
        """Get a config value as string."""
        value = self.get(key, default)
        if value is None:
            raise ConfigError(f"Key '{key}' not found and no default provided")
        if isinstance(value, (list, dict)):
            raise ConfigError(f"Key '{key}' is a {type(value).__name__}, cannot convert to string")
        return str(value)

    def get_list(self, key: str, default: list | None = None) -> list:
        """Get a config value as list."""
        value = self.get(key, default)
        if value is None:
            raise ConfigError(f"Key '{key}' not found and no default provided")
        if isinstance(value, str):
            raise ConfigError(f"Key '{key}' is a string, not a list. Did you mean to split it?")
        if not isinstance(value, list):
            raise ConfigError(f"Key '{key}' has type {type(value).__name__}, expected list")
        return value

    def require(self, *keys: str) -> None:
        """Verify that all required keys exist."""
        missing = []
        for key in keys:
            try:
                self.get(key)
            except ConfigError:
                missing.append(key)
        if missing:
            raise ConfigError(f"Missing required config keys: {', '.join(missing)}")

    def get_or_env(self, key: str, env_var: str) -> str:
        """Get from config, falling back to environment variable."""
        try:
            return self.get_str(key)
        except ConfigError:
            value = os.environ.get(env_var)
            if value is None:
                raise ConfigError(
                    f"Key '{key}' not in config and environment variable '{env_var}' not set"
                )
            if not value.strip():
                raise ConfigError(
                    f"Environment variable '{env_var}' is set but empty"
                )
            return value

    def merge(self, overrides: dict) -> None:
        """Merge override values into config."""
        if not isinstance(overrides, dict):
            raise ConfigError(f"Overrides must be a dict, got {type(overrides).__name__}")
        if not overrides:
            raise ConfigError("Overrides dict is empty — nothing to merge")
        self._deep_merge(self._data, overrides)

    def _deep_merge(self, base: dict, override: dict) -> None:
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def as_dict(self) -> dict:
        """Return a copy of the full config."""
        if not self._data:
            raise ConfigError("Config is empty")
        return dict(self._data)

    def reload(self) -> None:
        """Reload config from disk."""
        if not self._path.exists():
            raise ConfigError(f"Config file no longer exists: {self._path}")
        self._data.clear()
        self._load()
