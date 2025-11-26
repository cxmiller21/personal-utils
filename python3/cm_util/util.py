import logging
import json
import subprocess
import time
import yt_dlp

from pathlib import Path
from typing import Any, Optional, Dict
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

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


def get_yt_dl_options(media_type: str, show_progress: bool = True) -> dict:
    """Get download options for YouTube DL

    Args:
        media_type (str): Type of media ('mp3' or 'video')
        show_progress (bool): Whether to show download progress (default: True)

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

        # Add progress hook if enabled
        if show_progress:
            options["progress_hooks"] = [yt_dl_progress_hook]

        # Try to add Chrome cookies, but don't fail if Chrome is not available
        try:
            cookies = yt_dlp.parse_options(['--cookies-from-browser', 'chrome']).ydl_opts['cookiesfrombrowser']
            options["cookiesfrombrowser"] = cookies
        except Exception as e:
            log.warning(f"Could not load Chrome cookies (Chrome may not be installed): {str(e)}")
            log.warning("Continuing without browser cookies - some downloads may fail")

        return options

    if media_type == "video":
        options = {
            "format": "best*",
            "format_sort": ["vcodec:h264", "res", "acodec:m4a"],
            "ignoreerrors": False,
            "outtmpl": "%(title)s.%(ext)s",
            "merge_output_format": "mp4",
        }

        # Add progress hook if enabled
        if show_progress:
            options["progress_hooks"] = [yt_dl_progress_hook]

        return options


def yt_dl_progress_hook(d: dict[str, Any]) -> None:
    """YouTube DL hook to show download progress"""
    if d["status"] == "downloading":
        # Extract progress information
        percent = d.get("_percent_str", "N/A")
        speed = d.get("_speed_str", "N/A")
        eta = d.get("_eta_str", "N/A")

        # Print progress on same line
        print(f"\rDownloading: {percent} | Speed: {speed} | ETA: {eta}", end="", flush=True)
    elif d["status"] == "finished":
        print()  # New line after download completes
        log.info(f"Done downloading, now converting file {d.get('filename', 'file')}")


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
def tag_mp3_file(file_path: Path, metadata: Dict[str, Any]) -> None:
    """Add ID3 tags to an MP3 file

    Args:
        file_path: Path to the MP3 file
        metadata: Metadata dictionary from yt-dlp
    """
    try:
        # Try to load existing tags or create new ones
        try:
            audio = EasyID3(file_path)
        except ID3NoHeaderError:
            # No ID3 tags exist, create them
            audio = EasyID3()
            audio.save(file_path)
            audio = EasyID3(file_path)

        # Add available metadata
        if metadata.get('title'):
            audio['title'] = metadata['title']
        if metadata.get('artist') or metadata.get('uploader'):
            audio['artist'] = metadata.get('artist') or metadata.get('uploader')
        if metadata.get('album'):
            audio['album'] = metadata['album']
        if metadata.get('upload_date'):
            # Convert YYYYMMDD to YYYY
            date = metadata['upload_date']
            audio['date'] = date[:4] if len(date) >= 4 else date

        audio.save()
        log.debug(f"Tagged MP3 file: {file_path.name}")
    except Exception as e:
        log.warning(f"Could not tag MP3 file {file_path.name}: {str(e)}")


def clean_url(url: str, media_company: str) -> str:
    """Clean URL to be used for downloading

    Args:
        url (str): URL to clean
        media_company (str): Media company to clean URL for
    """
    if media_company.lower() != "youtube":
        return url

    # If YouTube URL
    if "watch\\?v\\=" in url:
        # Handle copy/paste from YouTube to terminal where backslashes are added
        return url.replace("watch\\?v\\=", "watch?v=")
    return url


def yt_dlp_download(url: str, media_company: str, media_type: str, max_retries: int = 3, retry_delay: int = 2, dry_run: bool = False, output_dir: str = None, force: bool = False) -> None:
    """YouTube DL download with retry logic

    Args:
        url (str): Media URL to download
        media_company (str): Media company to download from
        media_type (str): Media type to download
        max_retries (int): Maximum number of retry attempts (default: 3)
        retry_delay (int): Seconds to wait between retries (default: 2)
        dry_run (bool): If True, only show what would be downloaded (default: False)
        output_dir (str): Custom output directory (default: current directory)
        force (bool): If True, download even if URL exists in history (default: False)

    Raises:
        Exception: If download fails after all retries
    """
    from .history_manager import is_downloaded, get_download_info, add_to_history

    cleaned_url = clean_url(url, media_company)

    # Check download history unless force flag is set
    if not force and is_downloaded(url):
        info = get_download_info(url)
        log.info(f"⏭️  Skipping - already downloaded: {info.get('title', url)}")
        log.info(f"   Downloaded on: {info.get('timestamp', 'unknown')}")
        log.info(f"   Use --force to download anyway")
        return

    if dry_run:
        log.info(f"[DRY RUN] Would download {media_type} from {media_company}: {url}")
        if output_dir:
            log.info(f"[DRY RUN] Output directory: {output_dir}")
        return

    options = get_yt_dl_options(media_type)

    # Set custom output directory if provided
    if output_dir:
        output_path = Path(output_dir)
        if not output_path.exists():
            output_path.mkdir(parents=True, exist_ok=True)
        options["outtmpl"] = str(output_path / "%(title)s.%(ext)s")

    last_exception = None
    downloaded_title = None
    downloaded_path = None
    metadata = None

    for attempt in range(max_retries):
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                # Extract info to get title and metadata before downloading
                info = ydl.extract_info(cleaned_url, download=True)
                if info:
                    downloaded_title = info.get('title', 'Unknown')
                    metadata = info
                    # Build the expected file path
                    if output_dir:
                        downloaded_path = str(Path(output_dir) / f"{downloaded_title}.{media_type}")
                    else:
                        downloaded_path = f"{downloaded_title}.{media_type}"

            log.info(f"Successfully downloaded {media_company} {media_type}!")

            # Tag MP3 files with metadata
            if media_type == "mp3" and metadata and downloaded_path:
                file_path = Path(downloaded_path)
                if file_path.exists():
                    tag_mp3_file(file_path, metadata)
                else:
                    # File might be in current directory if output_dir wasn't specified
                    # and the actual filename might have a different extension before conversion
                    # Try to find it by looking for files with the title
                    current_dir_path = Path(f"{downloaded_title}.mp3")
                    if current_dir_path.exists():
                        tag_mp3_file(current_dir_path, metadata)

            # Add to history
            add_to_history(
                url=url,
                title=downloaded_title or "Unknown",
                media_type=media_type,
                file_path=downloaded_path
            )

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
