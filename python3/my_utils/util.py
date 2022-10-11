import json
from os import system
from pathlib import Path


def get_json_config(file_name: str) -> dict:
    """Get data from config file"""
    with open(f"{Path.cwd()}/config/{file_name}.json") as f:
        return json.load(f)


def open_app(dir: str, app: str) -> int:
    """open a single application"""
    print(f"Dir: {dir} - Opening {app}...")
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


# def sort_file_naming_convention(dir_path: str) -> list[str]:
#     """Sort file naming convention
    
#     Args:
#         dir_path (str): Directory to verify file nameing convention.
    
#     Returns:
#         list[str]: Sorted file name.
#     """
#     p = Path(dir_path)
#     for file in [x for x in p.iterdir() if x.is_file()]:
#         print(file)
#     return p
