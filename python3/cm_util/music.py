import logging

from .util import (
  yt_dlp_download,
  move_mp3_files_to_music_folder
)

log = logging.getLogger(__name__)


def download_mp3(url: str, media_company: str, dry_run: bool = False, output_dir: str = None, force: bool = False) -> None:
    """Download MP3 from URL

    Args:
        url: Media URL
        media_company: Media company name
        dry_run: If True, only show what would be downloaded
        output_dir: Custom output directory
        force: If True, download even if URL exists in history
    """
    yt_dlp_download(url, media_company, "mp3", dry_run=dry_run, output_dir=output_dir, force=force)
    if not dry_run:
        move_mp3_files_to_music_folder()


def download_youtube_playlist(url: str, dry_run: bool = False, output_dir: str = None, force: bool = False) -> None:
    """Download YouTube playlist as MP3s

    Args:
        url: Playlist URL
        dry_run: If True, only show what would be downloaded
        output_dir: Custom output directory
        force: If True, download even if URL exists in history
    """
    yt_dlp_download(url, "YouTube", "mp3", dry_run=dry_run, output_dir=output_dir, force=force)
    if not dry_run:
        move_mp3_files_to_music_folder()


def download_soundcloud_user_likes(username: str, dry_run: bool = False, output_dir: str = None, force: bool = False) -> None:
    """Download SoundCloud user likes as MP3s

    Args:
        username: SoundCloud username
        dry_run: If True, only show what would be downloaded
        output_dir: Custom output directory
        force: If True, download even if URL exists in history
    """
    url = f"https://soundcloud.com/{username}/likes"
    yt_dlp_download(url, "SoundCloud", "mp3", dry_run=dry_run, output_dir=output_dir, force=force)
    if not dry_run:
        move_mp3_files_to_music_folder()
