import logging
import re
import sys
import typer

from pathlib import Path
from cm_util import music, video, util
from cm_util.config_manager import load_config, show_config
from typing import Optional

# Configure logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger(__name__)

app = typer.Typer()

# Global state
class State:
    verbose: bool = False
    quiet: bool = False
    dry_run: bool = False
    output_dir: Optional[str] = None
    force: bool = False

state = State()

def version_callback(value: bool):
    """Show version and exit"""
    if value:
        from cm_util import __version__
        typer.echo(f"cm-util version {__version__}")
        raise typer.Exit()

def verbosity_callback(ctx: typer.Context, param: typer.CallbackParam, value: bool):
    """Set logging level based on verbosity flags"""
    if value:
        if param.name == "verbose":
            state.verbose = True
            logging.getLogger().setLevel(logging.DEBUG)
            log.debug("Verbose mode enabled")
        elif param.name == "quiet":
            state.quiet = True
            logging.getLogger().setLevel(logging.ERROR)
    return value

@app.callback()
def main(
    verbose: bool = typer.Option(
        False, "--verbose", "-v",
        help="Enable verbose output (DEBUG level)",
        callback=verbosity_callback,
        is_eager=True
    ),
    quiet: bool = typer.Option(
        False, "--quiet", "-q",
        help="Suppress all output except errors",
        callback=verbosity_callback,
        is_eager=True
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run",
        help="Show what would be done without actually doing it"
    ),
    output_dir: Optional[str] = typer.Option(
        None, "--output-dir", "-o",
        help="Custom output directory for downloads"
    ),
    force: bool = typer.Option(
        False, "--force", "-f",
        help="Force download even if URL exists in history"
    ),
    version: Optional[bool] = typer.Option(
        None, "--version",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True
    ),
):
    """
    Personal CLI utility for downloading media and managing files on macOS.
    """
    # Load config and merge with CLI options (CLI takes precedence)
    config = load_config()

    state.dry_run = dry_run
    state.output_dir = output_dir or config.get("output_dir")
    state.force = force

    if dry_run:
        log.info("🔍 DRY RUN MODE - No actual downloads will be performed")


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
    # YouTube URL pattern
    youtube_pattern = r"^https?://(www\.)?youtube\.com/.+"

    # SoundCloud URL pattern
    soundcloud_pattern = r"^https?://(www\.)?soundcloud\.com/.+"

    if re.match(youtube_pattern, url):
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
    return music.download_mp3(url, media_company, dry_run=state.dry_run, output_dir=state.output_dir, force=state.force)


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
    log.info(f"State: dry_run={state.dry_run}, output_dir={state.output_dir}, force={state.force}")
    return video.download_youtube_video(url, dry_run=state.dry_run, output_dir=state.output_dir, force=state.force)


@app.command()
def dl_sc_user_likes(
    username: str = typer.Option(
        ..., "--username", "-un", help="SoundCloud username to download likes from"
    )
) -> None:
    """Download a playlist of SoundCloud user likes and open them in Apple Music"""
    log.info(f"Downloading SoundCloud user likes: {username}...")
    music.download_soundcloud_user_likes(username, dry_run=state.dry_run, output_dir=state.output_dir, force=state.force)


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


@app.command()
def config(
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
    set_key: Optional[str] = typer.Option(None, "--set", help="Set a configuration key (e.g., output_dir, retry_count, retry_delay)"),
    value: Optional[str] = typer.Option(None, "--value", help="Value to set for the key"),
) -> None:
    """Manage configuration settings"""
    from cm_util.config_manager import set_config_value

    if show:
        show_config()
        return

    if set_key and value is not None:
        # Handle type conversions
        if set_key in ["retry_count", "retry_delay"]:
            try:
                value = int(value)
            except ValueError:
                log.error(f"Invalid value for {set_key}: must be an integer")
                raise typer.Exit(code=1)
        elif set_key == "show_progress":
            value = value.lower() in ["true", "1", "yes", "y"]

        set_config_value(set_key, value)
        log.info(f"Set {set_key} = {value}")
        show_config()
    elif set_key and value is None:
        log.error("Must provide --value when using --set")
        raise typer.Exit(code=1)
    else:
        show_config()


@app.command()
def history(
    show: bool = typer.Option(False, "--show", help="Show download history"),
    clear: bool = typer.Option(False, "--clear", help="Clear download history"),
    limit: Optional[int] = typer.Option(None, "--limit", "-n", help="Limit number of records to show"),
) -> None:
    """View and manage download history"""
    from cm_util.history_manager import show_history, clear_history

    if clear:
        if typer.confirm("Are you sure you want to clear all download history?"):
            clear_history()
            log.info("Download history cleared")
        else:
            log.info("Operation cancelled")
        return

    if show or not (show or clear):
        show_history(limit=limit)


if __name__ == "__main__":
    app()
