"""Download history management for cm-util"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

log = logging.getLogger(__name__)

DEFAULT_HISTORY_DIR = Path.home() / ".cm-util"
DEFAULT_HISTORY_FILE = DEFAULT_HISTORY_DIR / "history.json"


def ensure_history_dir() -> None:
    """Ensure history directory exists"""
    DEFAULT_HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def load_history() -> List[Dict]:
    """Load download history from file

    Returns:
        list: List of download records
    """
    if not DEFAULT_HISTORY_FILE.exists():
        return []

    try:
        with open(DEFAULT_HISTORY_FILE, "r") as f:
            history = json.load(f)
        return history
    except Exception as e:
        log.warning(f"Error loading history file: {e}. Starting with empty history.")
        return []


def save_history(history: List[Dict]) -> None:
    """Save download history to file

    Args:
        history: List of download records to save
    """
    ensure_history_dir()

    try:
        with open(DEFAULT_HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        log.error(f"Error saving history file: {e}")


def add_to_history(url: str, title: str, media_type: str, file_path: Optional[str] = None) -> None:
    """Add a download to history

    Args:
        url: URL that was downloaded
        title: Title of the downloaded media
        media_type: Type of media (mp3, video)
        file_path: Path where file was saved
    """
    history = load_history()

    record = {
        "url": url,
        "title": title,
        "media_type": media_type,
        "file_path": file_path,
        "timestamp": datetime.now().isoformat(),
    }

    history.append(record)
    save_history(history)
    log.debug(f"Added to history: {url}")


def is_downloaded(url: str) -> bool:
    """Check if a URL has been downloaded before

    Args:
        url: URL to check

    Returns:
        bool: True if URL exists in history
    """
    history = load_history()
    return any(record["url"] == url for record in history)


def get_download_info(url: str) -> Optional[Dict]:
    """Get download information for a URL

    Args:
        url: URL to look up

    Returns:
        dict or None: Download record if found
    """
    history = load_history()
    for record in history:
        if record["url"] == url:
            return record
    return None


def clear_history() -> None:
    """Clear all download history"""
    save_history([])
    log.info("Download history cleared")


def show_history(limit: Optional[int] = None) -> None:
    """Display download history

    Args:
        limit: Maximum number of records to show
    """
    history = load_history()

    if not history:
        log.info("Download history is empty")
        return

    log.info(f"Download History ({len(history)} total downloads)")
    log.info(f"History file: {DEFAULT_HISTORY_FILE}")

    # Show most recent first
    history_to_show = list(reversed(history))
    if limit:
        history_to_show = history_to_show[:limit]

    for i, record in enumerate(history_to_show, 1):
        timestamp = record.get("timestamp", "Unknown")
        url = record.get("url", "Unknown")
        title = record.get("title", "Unknown")
        media_type = record.get("media_type", "Unknown")

        log.info(f"{i}. [{timestamp}]")
        log.info(f"   Type: {media_type}")
        log.info(f"   Title: {title}")
        log.info(f"   URL: {url}")
        if record.get("file_path"):
            log.info(f"   File: {record['file_path']}")
