import logging

from pathlib import Path
from .util import yt_dlp_download, sort_files_by

log = logging.getLogger(__name__)


def move_video_files_to_downloads(custom_path: str = "") -> None:
    """Move downloaded video files to the Downloads folder

    Args:
        custom_path (str, optional): Custom path to move videos to. Defaults to ~/Downloads

    Raises:
        ValueError: Downloads folder path does not exist
    """
    downloads_folder = Path.home() / "Downloads" if not custom_path else Path(custom_path)

    if not downloads_folder.exists():
        raise ValueError(f"Path {downloads_folder} does not exist")

    # Sort video files by creation time (most common video formats)
    video_extensions = ["mp4"]
    moved_files = []

    for ext in video_extensions:
        try:
            sorted_file_paths = sort_files_by("./", ext, "date")
            for file_path in sorted_file_paths:
                file = file_path.name
                log.info(f"Moving file {file} to Downloads folder...")
                dest = downloads_folder / file
                file_path.rename(dest)
                moved_files.append(file)
        except Exception:
            # No files of this type found, continue
            continue

    if moved_files:
        log.info(f"Moved {len(moved_files)} video file(s) to {downloads_folder}")
    else:
        log.warning("No video files found to move")


def download_youtube_video(url: str) -> None:
    """Download YouTube video

    Args:
        url (str): YouTube video URL
    """
    yt_dlp_download(url, "YouTube", "video")
    log.info(f"YouTube Videos successfully downloaded")
    move_video_files_to_downloads()
