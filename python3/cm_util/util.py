import logging
import json
import yt_dlp

from os import system
from pathlib import Path

log = logging.getLogger(__name__)


def get_comp_user_name() -> str:
    """Get the name of the computer user"""
    cwd = Path.cwd()
    if cwd.parts[1] == "Users":
        return cwd.parts[2]
    raise ValueError("Unable to get computer user name")


def get_itunes_music_folder() -> str:
    """Get the path to the Apple Music folder.
    Currently only works for Ventura OS and up folder structure
    """
    comp_user = get_comp_user_name()
    log.info(f"Computer user: {comp_user}")
    return f"/Users/{comp_user}/Music/Music/Media.localized/Automatically Add to Music.localized"


def get_yt_dl_options(media_type: str) -> dict:
    """Get download options for YouTube DL"""
    if media_type not in ["mp3", "video"]:
        raise ValueError("Media type must be either 'mp3' or 'video'")
    if media_type == "mp3":
        return {
            "format": "bestaudio/best",
            "ignoreerrors": True,
            "outtmpl": "%(title)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
    if media_type == "video":
        return {
            "format": "best",
            "ignoreerrors": True,
            "outtmpl": "%(title)s.%(ext)s",
        }


def yt_dl_hook(d, logger) -> None:
    """YouTube DL hook to log download completion"""
    if d["status"] == "finished":
        logger.info(f"Done downloading, now converting file {d['filename']}")


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


def sort_files_by(path_to_folder: str, file_type: str, sort_by: str) -> None:
    """Sort files in folder by name, date, file type, or size

    Args:
        path_to_folder (str): Path to folder
        file_type (str): File type to filter by
        sort_by (str): Sort by name, date, file type, or size
    """
    directory = Path(path_to_folder)
    filtered_files = []
    if file_type == "all":
        filtered_files = [file for file in directory.iterdir() if file.is_file()]
    else:
        filtered_files = [
            file
            for file in directory.iterdir()
            if file.is_file() and file.suffix.lower() == f".{file_type}"
        ]

    if sort_by == "name":
        filtered_files.sort(key=lambda f: f.name)
    elif sort_by == "date":
        filtered_files.sort(key=lambda f: f.stat().st_ctime)
    return filtered_files


# YouTube DL/SoundCloud DL
def clean_url(url: str, media_company: str) -> str:
    """Clean URL to be used for downloading

    Args:
        url (str): URL to clean
        media_company (str): Media company to clean URL for
    """
    if media_company.lower() != "youtube":
        return url

    # If YouTube URL
    if "watch\?v\=" in url:
        # Handle copy/paste from YouTube to terminal where backslashes are added
        return url.replace("watch\?v\=", "watch?v=")
    return url


def yt_dlp_download(url: str, media_company: str, media_type: str) -> None:
    """YouTube DL download

    Args:
        url (str): Media URL to download
        media_company (str): Media company to download from
        media_type (str): Media type to download
    """
    cleaned_url = clean_url(url, media_company)
    options = get_yt_dl_options(media_type)

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            error_code = ydl.download([cleaned_url])
    except Exception as e:
        log.error(f"Error code: {error_code} - Unable to download url: {url}")
        raise Exception(e)
    log.info(f"Successfully downloaded {media_company} {media_type}!")


def move_mp3_files_to_music_folder(custom_path: str = "") -> None:
    """Move downloaded mp3 files to the Apple Music folder

    Args:
        custom_path (str, optional): Path to mp3s - Defaults to ""

    Raises:
        ValueError: Music folder path does not exist
    """
    music_folder_path = (
        Path(get_itunes_music_folder()) if not custom_path else Path(custom_path)
    )
    if not music_folder_path.exists():
        raise ValueError(f"Path {music_folder_path} does not exist")

    # Sort files by creation time
    # sorted_file_paths = sorted(mp3_file_paths, key=lambda x: x.stat().st_ctime)
    sorted_file_paths = sort_files_by("./", "mp3", "date")
    for file_path in sorted_file_paths:
        file = file_path.name
        log.info(f"Moving file {file} to Itunes Music folder...")
        dest = music_folder_path / file
        file_path.rename(dest)
