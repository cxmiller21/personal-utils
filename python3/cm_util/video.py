import logging
from pathlib import Path

from .util import sort_files_by, yt_dlp_download

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


def download_youtube_video(
    url: str, dry_run: bool = False, output_dir: str = None, force: bool = False
) -> None:
    """Download YouTube video

    Args:
        url (str): YouTube video URL
        dry_run (bool): If True, only show what would be downloaded
        output_dir (str): Custom output directory
        force (bool): If True, download even if URL exists in history
    """
    yt_dlp_download(url, "YouTube", "video", dry_run=dry_run, output_dir=output_dir, force=force)
    if not dry_run:
        log.info(f"YouTube Videos successfully downloaded")
        # If custom output is specified, don't move files
        if not output_dir:
            move_video_files_to_downloads()
