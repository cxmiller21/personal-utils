import logging
import unittest

from cm_util import music
from unittest.mock import patch

log = logging.getLogger(__name__)


class TestDownloadMp3(unittest.TestCase):
    @patch("cm_util.music.move_mp3_files_to_music_folder")
    @patch("cm_util.music.yt_dlp_download")
    def test_download_mp3_youtube(self, mock_yt_dlp_download, mock_move_files):
        """Test downloading MP3 from YouTube"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        media_company = "YouTube"

        music.download_mp3(url, media_company)

        # Verify yt_dlp_download was called with correct parameters
        mock_yt_dlp_download.assert_called_once_with(url, media_company, "mp3", dry_run=False, output_dir=None, force=False)

        # Verify files were moved to Music folder
        mock_move_files.assert_called_once()

    @patch("cm_util.music.move_mp3_files_to_music_folder")
    @patch("cm_util.music.yt_dlp_download")
    def test_download_mp3_soundcloud(self, mock_yt_dlp_download, mock_move_files):
        """Test downloading MP3 from SoundCloud"""
        url = "https://soundcloud.com/artist/track"
        media_company = "SoundCloud"

        music.download_mp3(url, media_company)

        # Verify yt_dlp_download was called with correct parameters
        mock_yt_dlp_download.assert_called_once_with(url, media_company, "mp3", dry_run=False, output_dir=None, force=False)

        # Verify files were moved to Music folder
        mock_move_files.assert_called_once()

    @patch("cm_util.music.move_mp3_files_to_music_folder")
    @patch("cm_util.music.yt_dlp_download")
    def test_download_mp3_download_fails(self, mock_yt_dlp_download, mock_move_files):
        """Test that download failure propagates exception"""
        url = "https://www.youtube.com/watch?v=invalid"
        media_company = "YouTube"
        mock_yt_dlp_download.side_effect = Exception("Download failed")

        with self.assertRaises(Exception) as cm:
            music.download_mp3(url, media_company)

        self.assertIn("Download failed", str(cm.exception))
        # Verify move was not called since download failed
        mock_move_files.assert_not_called()


class TestDownloadYoutubePlaylist(unittest.TestCase):
    @patch("cm_util.music.move_mp3_files_to_music_folder")
    @patch("cm_util.music.yt_dlp_download")
    def test_download_youtube_playlist(self, mock_yt_dlp_download, mock_move_files):
        """Test downloading YouTube playlist"""
        url = "https://www.youtube.com/playlist?list=PLtest123"

        music.download_youtube_playlist(url)

        # Verify yt_dlp_download was called with correct parameters
        mock_yt_dlp_download.assert_called_once_with(url, "YouTube", "mp3", dry_run=False, output_dir=None, force=False)

        # Verify files were moved to Music folder
        mock_move_files.assert_called_once()


class TestDownloadSoundcloudUserLikes(unittest.TestCase):
    @patch("cm_util.music.move_mp3_files_to_music_folder")
    @patch("cm_util.music.yt_dlp_download")
    def test_download_soundcloud_user_likes(self, mock_yt_dlp_download, mock_move_files):
        """Test downloading SoundCloud user likes"""
        username = "test_user"
        expected_url = "https://soundcloud.com/test_user/likes"

        music.download_soundcloud_user_likes(username)

        # Verify yt_dlp_download was called with correct URL
        mock_yt_dlp_download.assert_called_once_with(expected_url, "SoundCloud", "mp3", dry_run=False, output_dir=None, force=False)

        # Verify files were moved to Music folder
        mock_move_files.assert_called_once()

    @patch("cm_util.music.move_mp3_files_to_music_folder")
    @patch("cm_util.music.yt_dlp_download")
    def test_download_soundcloud_user_likes_with_special_chars(
        self, mock_yt_dlp_download, mock_move_files
    ):
        """Test downloading SoundCloud user likes with special characters in username"""
        username = "test-user_123"
        expected_url = "https://soundcloud.com/test-user_123/likes"

        music.download_soundcloud_user_likes(username)

        # Verify yt_dlp_download was called with correct URL
        mock_yt_dlp_download.assert_called_once_with(expected_url, "SoundCloud", "mp3", dry_run=False, output_dir=None, force=False)

        # Verify files were moved to Music folder
        mock_move_files.assert_called_once()


if __name__ == "__main__":
    unittest.main()
