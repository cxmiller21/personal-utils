"""Configuration management for cm-util"""

import logging
from pathlib import Path
from typing import Any, Dict

import yaml

log = logging.getLogger(__name__)

DEFAULT_CONFIG_DIR = Path.home() / ".cm-util"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.yaml"

DEFAULT_CONFIG = {
    "retry_count": 3,
    "retry_delay": 2,
    "show_progress": True,
    "log_level": "INFO",
    "output_dir": None,
}


def get_config_path() -> Path:
    """Get path to config file"""
    return DEFAULT_CONFIG_FILE


def ensure_config_dir() -> None:
    """Ensure config directory exists"""
    DEFAULT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict[str, Any]:
    """Load configuration from file

    Returns:
        dict: Configuration dictionary
    """
    if not DEFAULT_CONFIG_FILE.exists():
        log.debug(f"No config file found at {DEFAULT_CONFIG_FILE}, using defaults")
        return DEFAULT_CONFIG.copy()

    try:
        with open(DEFAULT_CONFIG_FILE, "r") as f:
            config = yaml.safe_load(f) or {}

        # Merge with defaults (defaults for missing keys)
        merged_config = DEFAULT_CONFIG.copy()
        merged_config.update(config)

        log.debug(f"Loaded config from {DEFAULT_CONFIG_FILE}")
        return merged_config
    except Exception as e:
        log.warning(f"Error loading config file: {e}. Using defaults.")
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file

    Args:
        config: Configuration dictionary to save
    """
    ensure_config_dir()

    try:
        with open(DEFAULT_CONFIG_FILE, "w") as f:
            yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)
        log.info(f"Configuration saved to {DEFAULT_CONFIG_FILE}")
    except Exception as e:
        log.error(f"Error saving config file: {e}")


def get_config_value(key: str, default: Any = None) -> Any:
    """Get a single config value

    Args:
        key: Configuration key
        default: Default value if key not found

    Returns:
        Configuration value
    """
    config = load_config()
    return config.get(key, default)


def set_config_value(key: str, value: Any) -> None:
    """Set a single config value

    Args:
        key: Configuration key
        value: Value to set
    """
    config = load_config()
    config[key] = value
    save_config(config)


def show_config() -> None:
    """Display current configuration"""
    config = load_config()
    print("\n📁 Current Configuration:")
    print(f"   Config file: {DEFAULT_CONFIG_FILE}")
    print(f"   Exists: {DEFAULT_CONFIG_FILE.exists()}\n")

    for key, value in config.items():
        print(f"   {key}: {value}")
    print()
