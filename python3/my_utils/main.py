import logging
import sys
import typer
from my_utils import my_music
from my_utils import util

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def open_apps(
    type: str = typer.Option("default", "--type", "-t", prompt="Open my apps")
):
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
):
    """Download audio file and open in Itunes"""
    sc_url = "https://soundcloud.com"
    yt_url = "https://www.youtube.com"
    if not url.startswith(sc_url) and not url.startswith(yt_url):
        raise ValueError("URL must be for YouTube or SoundCloud URL")
    
    location = "YouTube" if "https://youtube.com" in url else "SoundCloud"
    log.info(f"Downloading {location} audio...")
    my_music.download_audio(url)


if __name__ == "__main__":
    app()
