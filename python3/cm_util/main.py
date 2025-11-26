import logging
import re
import sys
import typer

from pathlib import Path
from cm_util import music, video, util

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def open_apps(
    type: str = typer.Option("default", "--type", "-t", prompt="Open my apps")
) -> None:
    """Start up basic applications"""
    log.info(f"Welcome! Starting up Applications...")
    match type:
        case "default":
            log.info(f"Opening System Applications...")
            util.open_apps("installed")
            log.info(f"Opening Installed Applications...")
            util.open_apps("system")
        case "music":
            log.info(f"Opening Music Applications...")
            util.open_apps("music")


def validate_url(url: str) -> tuple[bool, str | None]:
    """Validate URL and determine media company

    Args:
        url (str): URL to validate

    Returns:
        tuple[bool, str | None]: (is_valid, media_company)
    """
    # YouTube URL patterns
    youtube_patterns = [
        r"^https?://(www\.)?youtube\.com/watch\?v=[\w-]+",
        r"^https?://(www\.)?youtube\.com/playlist\?list=[\w-]+",
        r"^https?://youtu\.be/[\w-]+",
    ]

    # SoundCloud URL pattern
    soundcloud_pattern = r"^https?://(www\.)?soundcloud\.com/.+"

    for pattern in youtube_patterns:
        if re.match(pattern, url):
            return True, "YouTube"

    if re.match(soundcloud_pattern, url):
        return True, "SoundCloud"

    return False, None


@app.command()
def dl_song(
    url: str = typer.Option(
        ..., "--url", "-u", help="URL wrapped in quotes '' to download"
    )
) -> None:
    """Download audio file and open in Apple Music"""
    is_valid, media_company = validate_url(url)

    if not is_valid or not media_company:
        log.error(f"URL: {url} is not a valid YouTube or SoundCloud URL")
        raise ValueError(
            "Invalid URL. Expected format: "
            "https://youtube.com/watch?v=... or https://soundcloud.com/..."
        )

    log.info(f"Downloading {media_company} audio...")
    return music.download_mp3(url, media_company)


@app.command()
def dl_video(
    url: str = typer.Option(
        ..., "--url", "-u", help="URL wrapped in quotes '' to download"
    )
) -> None:
    """Download video file"""
    is_valid, media_company = validate_url(url)

    if not is_valid or media_company != "YouTube":
        log.error(f"URL: {url} is not a valid YouTube URL")
        raise ValueError(
            "Invalid URL. Expected format: https://youtube.com/watch?v=..."
        )

    log.info(f"Downloading YouTube video...")
    return video.download_youtube_video(url)


@app.command()
def dl_sc_user_likes(
    username: str = typer.Option(
        ..., "--username", "-un", help="SoundCloud username to download likes from"
    )
) -> None:
    """Download a playlist of SoundCloud user likes and open them in Apple Music"""
    log.info(f"Downloading SoundCloud user likes: {username}...")
    music.download_soundcloud_user_likes(username)


@app.command()
def order_files(
    path_to_folder: str = typer.Option(
        ..., "--path", "-p", help="Absolute path to folder to order files"
    ),
    file_type: str = typer.Option(
        ..., "--file-type", "-ft", help="File type to filter by - Pass 'all' to include all files"
    ),
    order_by: str = typer.Option(
        ..., "--order-by", "-ob", help="Order files by name, date, or size"
    ),
) -> None:
    """Order files by name or created on date"""
    if not Path(path_to_folder).exists():
        raise ValueError("Path must be a valid directory")
    if order_by not in ["name", "date"]:
        raise ValueError("Order by must be either 'name', 'date'")

    log.info(f"Ordering files in folder '{path_to_folder}' by '{order_by}'...")
    util.sort_files_by(path_to_folder, file_type, order_by)


if __name__ == "__main__":
    app()
