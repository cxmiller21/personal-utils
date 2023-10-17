import logging
import sys
import typer

from pathlib import Path
from cm_util import music, util

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def open_apps(
    type: str = typer.Option("default", "--type", "-t", prompt="Open my apps")
) -> None:
    """Start up applications"""
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


@app.command()
def dl_song(
    url: str = typer.Option(
        ..., "--url", "-u", help="URL wrapped in quotes '' to download"
    )
) -> None:
    """Download audio file and open in Itunes"""
    # Optionally add regex to check if url is valid
    sc_url = "soundcloud.com/"
    yt_url = "youtube.com/"

    media_company = None
    if yt_url in url:
        media_company = "YouTube"
    elif sc_url in url:
        media_company = "SoundCloud"

    if not media_company:
        log.error(f"URL: {url} is not a valid YouTube or SoundCloud URL")
        raise ValueError("Invalid URL")

    log.info(f"Downloading {media_company} audio...")
    return music.download_mp3(url, media_company)


@app.command()
def dl_sc_user_likes(
    username: str = typer.Option(
        ..., "--username", "-un", help="SoundCloud username to download likes from"
    )
) -> None:
    """Download audio file and open in Itunes"""
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
    """Order files by name, date, or size"""
    if not Path(path_to_folder).exists():
        raise ValueError("Path must be a valid directory")
    if order_by not in ["name", "date", "type", "size"]:
        raise ValueError("Order by must be either 'name', 'date', 'type', or 'size'")

    log.info(f"Ordering files in folder '{path_to_folder}' by '{order_by}'...")
    util.sort_files_by(path_to_folder, file_type, order_by)


if __name__ == "__main__":
    app()
