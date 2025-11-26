import logging
import tempfile
import unittest

from cm_util import video
from pathlib import Path
from unittest.mock import patch, MagicMock

log = logging.getLogger(__name__)


class TestMoveVideoFilesToDownloads(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = self.temp_dir.name

    def test_move_video_files_default_path(self):
        """Test moving video files to default Downloads folder"""
        # Create test video files
        test_files = ["test1.mp4"]
        for file_name in test_files:
            file_path = Path(".") / file_name
            file_path.touch()

        # Create a temporary downloads folder
        downloads_folder = Path(self.temp_dir_path) / "Downloads"
        downloads_folder.mkdir()

        try:
            # Move files to temp downloads folder
            video.move_video_files_to_downloads(str(downloads_folder))

            # Verify files were moved
            moved_files = list(downloads_folder.glob("*"))
            self.assertEqual(len(moved_files), len(test_files))

            # Verify files no longer in current directory
            for file_name in test_files:
                self.assertFalse(Path(file_name).exists())
        finally:
            # Cleanup - move files back if they exist in downloads
            for file_name in test_files:
                dest_file = downloads_folder / file_name
                if dest_file.exists():
                    dest_file.unlink()

    def test_move_video_files_invalid_path(self):
        """Test that invalid path raises ValueError"""
        with self.assertRaises(ValueError) as cm:
            video.move_video_files_to_downloads("/invalid/path/that/does/not/exist")
        self.assertIn("does not exist", str(cm.exception))

    def test_move_video_files_no_videos(self):
        """Test behavior when no video files are present"""
        downloads_folder = Path(self.temp_dir_path) / "Downloads"
        downloads_folder.mkdir()

        # Should complete without error, just log a warning
        with self.assertLogs("cm_util.video", level="WARNING") as cm:
            video.move_video_files_to_downloads(str(downloads_folder))
        self.assertTrue(any("No video files found" in msg for msg in cm.output))

    def test_move_video_files_custom_path(self):
        """Test moving video files to custom path"""
        # Create test video file
        test_file = Path(".") / "custom_test.mp4"
        test_file.touch()

        custom_folder = Path(self.temp_dir_path) / "CustomFolder"
        custom_folder.mkdir()

        try:
            video.move_video_files_to_downloads(str(custom_folder))

            # Verify file was moved
            moved_file = custom_folder / "custom_test.mp4"
            self.assertTrue(moved_file.exists())
            self.assertFalse(test_file.exists())
        finally:
            # Cleanup
            if (custom_folder / "custom_test.mp4").exists():
                (custom_folder / "custom_test.mp4").unlink()

    def tearDown(self):
        self.temp_dir.cleanup()


class TestDownloadYoutubeVideo(unittest.TestCase):
    @patch("cm_util.video.move_video_files_to_downloads")
    @patch("cm_util.video.yt_dlp_download")
    def test_download_youtube_video(self, mock_yt_dlp_download, mock_move_files):
        """Test downloading YouTube video"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

        video.download_youtube_video(url)

        # Verify yt_dlp_download was called with correct parameters
        mock_yt_dlp_download.assert_called_once_with(url, "YouTube", "video")

        # Verify files were moved
        mock_move_files.assert_called_once()

    @patch("cm_util.video.move_video_files_to_downloads")
    @patch("cm_util.video.yt_dlp_download")
    def test_download_youtube_video_download_fails(self, mock_yt_dlp_download, mock_move_files):
        """Test that download failure propagates exception"""
        url = "https://www.youtube.com/watch?v=invalid"
        mock_yt_dlp_download.side_effect = Exception("Download failed")

        with self.assertRaises(Exception) as cm:
            video.download_youtube_video(url)

        self.assertIn("Download failed", str(cm.exception))
        # Verify move was not called since download failed
        mock_move_files.assert_not_called()


if __name__ == "__main__":
    unittest.main()
