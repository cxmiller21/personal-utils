import logging
import json
from os import system
from pathlib import Path
from shutil import move

log = logging.getLogger(__name__)


def get_json_config(file_name: str) -> dict:
    """Get data from config file"""
    with open(f"{Path.cwd()}/config/{file_name}.json") as f:
        return json.load(f)


def open_app(dir: str, app: str) -> int:
    """open a single application"""
    log.info(f"Dir: {dir} - Opening {app}...")
    return system(f"open {dir}/{app}.app")


def open_apps(type: str) -> None:
    """open applications

    Args:
        type (str): Type of applications to open. Can be "installed" or "system"
    """
    if type not in ["installed", "system", "music"]:
        raise ValueError("Type must be either 'installed' or 'system'")

    data = get_json_config("my-apps")[type]

    for app in data["apps"]:
        open_app(data["path"], app)


def sort_file_naming_convention(path_to_folder: str, sort_by: str) -> None:
    """Sort files in folder by name, date, file type, or size
    Example only - does not work from Mac finder
    """
    sorting_functions = {
        "name" : lambda x: x.name,
        "date": lambda x: x.stat().st_mtime,
        "type": lambda x: x.suffix,
        "size": lambda x: x.stat().st_size,
    }
    sorted(Path(path_to_folder).glob("*"), key=sorting_functions[sort_by])
