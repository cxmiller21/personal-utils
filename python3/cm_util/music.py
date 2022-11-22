from __future__ import unicode_literals

import logging
import youtube_dl
from os import rename
from pathlib import Path

log = logging.getLogger(__name__)


def yt_dl_hook(d) -> None:
    if d["status"] == "finished":
        log.info(f"Done downloading, now converting file {d['filename']} ...")


YDL_OPTIONS = {
    "format": "bestaudio/best",
    "outtmpl": "%(title)s.%(ext)s",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "logger": log,
    "progress_hooks": [yt_dl_hook],
}


def download_audio(url: str) -> None:
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        ydl.download([url])
    log.info("Done downloading YouTube audio!")
    mp3_files = Path(".").glob("*.mp3")
    for file in mp3_files:
        log.info(f"Moving file {file} to Itunes Music folder...")
        src = f"/Users/coopermiller/Music/Music/Media.localized/Automatically Add to Music.localized/{file}"
        rename(f"{Path.cwd()}/{file}", src)
