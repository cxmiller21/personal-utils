import json
from os import system, getcwd


def get_json_config(file_name: str) -> dict:
    """Get data from config file"""
    cwd = getcwd()
    with open(f"{cwd}/config/{file_name}.json") as f:
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

