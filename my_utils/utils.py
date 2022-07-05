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
    # return system(f"open {dir}/{app}.app")


def open_installed_apps() -> None:
    """open default installed applications"""
    app_list = get_json_config("my-apps")
    dir = app_list["installed"]["path"]

    for app in app_list["installed"]["apps"]:
        open_app(dir, app)


def open_system_apps() -> None:
    """open default system applications"""
    app_list = get_json_config("my-apps")
    dir = app_list["system"]["path"]

    for app in app_list["system"]["apps"]:
        open_app(dir, app)
