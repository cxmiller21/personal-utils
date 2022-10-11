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
    """Start up applications

    Args:
        type (str): Type of applications to open based on my-apps.json key values.
    """
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
def dl_song(url: str = typer.Option("", "--url", prompt="YouTube URL to download")):
    """Download YouTube audio

    Args:
        url (str): YouTube URL.
    """
    if "youtube.com" in url:
        log.info(f"Downloading YouTube audio...")
        my_music.download_youtube_audio(url)
    if "soundcloud.com" in url:
        log.info(f"Downloading SoundCloud audio...")
        my_music.download_soundcloud_audio(url)


if __name__ == "__main__":
    app()
