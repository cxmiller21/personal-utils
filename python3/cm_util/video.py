import logging

from .util import yt_dlp_download

log = logging.getLogger(__name__)


def download_youtube_video(url: str) -> None:
    """Download YouTube video

    Args:
        url (str): YouTube video URL
    """
    yt_dlp_download(url, "YouTube", "video")
    log.info(f"YouTube Videos successfully downloaded")
    log.info("Please view videos in the ./tmp/ folder")

    # Move downloaded .mp4 video file to ~/Downloads folder
    

