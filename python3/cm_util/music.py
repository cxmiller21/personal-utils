import logging

from .util import (
  yt_dlp_download,
  move_mp3_files_to_music_folder
)

log = logging.getLogger(__name__)


def download_mp3(url: str, media_company: str) -> None:
    yt_dlp_download(url, media_company, "mp3")
    move_mp3_files_to_music_folder()


def download_youtube_playlist(url: str) -> None:
    yt_dlp_download(url, "YouTube", "mp3")
    move_mp3_files_to_music_folder()


def download_soundcloud_user_likes(username: str) -> None:
    url = f"https://soundcloud.com/{username}/likes"
    yt_dlp_download(url, "SoundCloud", "mp3")
    move_mp3_files_to_music_folder()
