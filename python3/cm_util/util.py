import logging
import json
import subprocess
import time
import yt_dlp

from pathlib import Path
from typing import Any

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
    """Get download options for YouTube DL

    Args:
        media_type (str): Type of media ('mp3' or 'video')

    Returns:
        dict: yt-dlp options dictionary

    Raises:
        ValueError: If media_type is not 'mp3' or 'video'
    """
    if media_type not in ["mp3", "video"]:
        raise ValueError("Media type must be either 'mp3' or 'video'")

    if media_type == "mp3":
        # example cli command
        # yt-dlp -f bestaudio/best --ignore-errors --out "%(title)s.%(ext)s" --postprocessor-args "-ar 44100 -ac 2" --postprocessor-args "-b:a 192k" --cookies-from-browser chrome
        options = {
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

        # Try to add Chrome cookies, but don't fail if Chrome is not available
        try:
            cookies = yt_dlp.parse_options(['--cookies-from-browser', 'chrome']).ydl_opts['cookiesfrombrowser']
            options["cookiesfrombrowser"] = cookies
        except Exception as e:
            log.warning(f"Could not load Chrome cookies (Chrome may not be installed): {str(e)}")
            log.warning("Continuing without browser cookies - some downloads may fail")

        return options

    if media_type == "video":
        return {
            "format": "best",
            "ignoreerrors": True,
            "outtmpl": "%(title)s.%(ext)s",
        }


def yt_dl_hook(d: dict[str, Any], logger: logging.Logger) -> None:
    """YouTube DL hook to log download completion"""
    if d["status"] == "finished":
        logger.info(f"Done downloading, now converting file {d['filename']}")


def get_json_config(file_name: str) -> dict:
    """Get data from config file

    Args:
        file_name (str): Name of the config file (without .json extension)

    Returns:
        dict: Configuration data

    Raises:
        FileNotFoundError: If config file doesn't exist
    """
    # Get config path relative to this module's location
    config_path = Path(__file__).parent / "config" / f"{file_name}.json"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        return json.load(f)


def open_app(dir: str, app: str) -> int:
    """open a single application"""
    log.info(f"Dir: {dir} - Opening {app}...")
    try:
        result = subprocess.run(
            ["open", f"{dir}/{app}.app"],
            check=True,
            capture_output=True,
            text=True
        )
        return result.returncode
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to open {app}: {e.stderr}")
        return e.returncode
    except FileNotFoundError:
        log.error("'open' command not found. This utility requires macOS.")
        return 1


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


def sort_files_by(path_to_folder: str, file_type: str, sort_by: str) -> list[Path]:
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
    if r"watch\?v\=" in url:
        # Handle copy/paste from YouTube to terminal where backslashes are added
        return url.replace(r"watch\?v\=", "watch?v=")
    return url


def yt_dlp_download(url: str, media_company: str, media_type: str, max_retries: int = 3, retry_delay: int = 2) -> None:
    """YouTube DL download with retry logic

    Args:
        url (str): Media URL to download
        media_company (str): Media company to download from
        media_type (str): Media type to download
        max_retries (int): Maximum number of retry attempts (default: 3)
        retry_delay (int): Seconds to wait between retries (default: 2)

    Raises:
        Exception: If download fails after all retries
    """
    cleaned_url = clean_url(url, media_company)
    options = get_yt_dl_options(media_type)

    last_exception = None
    for attempt in range(max_retries):
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                error_code = ydl.download([cleaned_url])
                if error_code != 0:
                    log.error(f"Error code: {error_code} - Failed to download url: {url}")
                    raise Exception(f"Download failed with error code: {error_code}")
            log.info(f"Successfully downloaded {media_company} {media_type}!")
            return  # Success - exit function
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                log.warning(f"Download attempt {attempt + 1} failed: {str(e)}. Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                log.error(f"Unable to download url: {url} after {max_retries} attempts - {str(e)}")

    # If we get here, all retries failed
    raise last_exception


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
