import logging
import sys
import typer
from pathlib import Path
from cm_util import music
from cm_util import util

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
        ..., "--url", "-u", help="YouTube URL (wrapped in quotes) to download"
    )
) -> None:
    """Download audio file and open in Itunes"""
    sc_url = "https://soundcloud.com"
    yt_url = "https://www.youtube.com"
    if not url.startswith(sc_url) and not url.startswith(yt_url):
        raise ValueError("URL must be for YouTube or SoundCloud URL")

    location = "YouTube" if "https://youtube.com" in url else "SoundCloud"
    log.info(f"Downloading {location} audio...")
    music.download_audio(url)


@app.command()
def order_files(
    path_to_folder: str = typer.Option(
        ..., "--path", "-p", help="Absolute path to folder to order files"
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
    util.sort_file_naming_convention(path_to_folder, order_by)


if __name__ == "__main__":
    app()
