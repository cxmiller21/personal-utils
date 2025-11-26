import logging
import tempfile
import unittest

from cm_util import util
from pathlib import Path
from unittest.mock import patch, call, Mock, MagicMock

log = logging.getLogger(__name__)


class TestGetItunesMusicFolder(unittest.TestCase):
    def test_get_itunes_music_folder(self):
        dev_user = util.get_comp_user_name()
        expected_path = f"/Users/{dev_user}/Music/Music/Media.localized/Automatically Add to Music.localized"
        result = util.get_itunes_music_folder()
        self.assertEqual(
            result, expected_path, "Returned path should match the expected path"
        )


class TestGetYtDLOptions(unittest.TestCase):
    def test_get_mp3_options(self):
        media_type = "mp3"
        options = util.get_yt_dl_options(media_type)

        # Test required keys
        self.assertEqual(options["format"], "bestaudio/best")
        self.assertEqual(options["ignoreerrors"], True)
        self.assertEqual(options["outtmpl"], "%(title)s.%(ext)s")

        # Test postprocessors
        self.assertEqual(len(options["postprocessors"]), 1)
        self.assertEqual(options["postprocessors"][0]["key"], "FFmpegExtractAudio")
        self.assertEqual(options["postprocessors"][0]["preferredcodec"], "mp3")
        self.assertEqual(options["postprocessors"][0]["preferredquality"], "192")

        # Test cookiesfrombrowser exists
        self.assertIn("cookiesfrombrowser", options, "cookiesfrombrowser should be present for MP3 downloads")

    def test_get_video_options(self):
        media_type = "video"
        options = util.get_yt_dl_options(media_type)

        expected_options = {
            "format": "best",
            "ignoreerrors": True,
            "outtmpl": "%(title)s.%(ext)s",
        }

        self.assertEqual(
            options, expected_options, "Video options should match expected"
        )

    def test_invalid_media_type(self):
        media_type = "invalid_type"
        with self.assertRaises(ValueError):
            util.get_yt_dl_options(media_type)


class TestGetJsonConfig(unittest.TestCase):
    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='{"installed": {"path": "/Applications", "apps": ["App1"]}, "system": {"path": "/System/Applications", "apps": ["App2"]}}')
    def test_get_app_config_data(self, mock_file):
        app_data = util.get_json_config("my-apps")
        assert type(app_data) == dict

        assert app_data["installed"]["path"] == "/Applications"
        assert app_data["system"]["path"] == "/System/Applications"

        assert type(app_data["installed"]["apps"]) == list
        assert type(app_data["system"]["apps"]) == list


class TestYtDlHook(unittest.TestCase):
    def test_yt_dl_hook(self):
        # Define a sample download dictionary
        download_info = {"status": "finished", "filename": "example_audio.mp3"}

        # Capture the log output for testing
        with self.assertLogs("test", level="INFO") as cm:
            logger = logging.getLogger("test")
            util.yt_dl_hook(download_info, logger)
        msg = f"INFO:test:Done downloading, now converting file {download_info['filename']}"
        self.assertEqual(cm.output, [msg])


class TestCleanUrl(unittest.TestCase):
    def test_clean_url_non_youtube(self):
        url = "https://example.com/video"
        media_company = "other"
        result = util.clean_url(url, media_company)
        self.assertEqual(result, url, "Non-YouTube URL should not be modified")

    def test_clean_url_youtube_with_backslashes(self):
        url = "https://www.youtube.com/watch\?v\=xyz"
        media_company = "youtube"
        result = util.clean_url(url, media_company)
        self.assertEqual(
            result,
            "https://www.youtube.com/watch?v=xyz",
            "Backslashes should be replaced",
        )

    def test_clean_url_youtube_no_backslashes(self):
        url = "https://www.youtube.com/watch?v=xyz"
        media_company = "youtube"
        result = util.clean_url(url, media_company)
        self.assertEqual(result, url, "URL without backslashes should not be modified")


class TestOpenApps(unittest.TestCase):
    @patch("cm_util.util.get_json_config")
    @patch("cm_util.util.open_app")
    def test_open_installed_apps(self, mock_open_app, mock_get_json_config):
        mock_get_json_config.return_value = {
            "installed": {"apps": ["App1", "App2"], "path": "/path/to/installed/apps"}
        }

        util.open_apps("installed")

        expected_calls = [
            call("/path/to/installed/apps", "App1"),
            call("/path/to/installed/apps", "App2"),
        ]
        mock_open_app.assert_has_calls(expected_calls)

    @patch("cm_util.util.get_json_config")
    @patch("cm_util.util.open_app")
    def test_open_system_apps(self, mock_open_app, mock_get_json_config):
        mock_get_json_config.return_value = {
            "system": {
                "apps": ["SystemApp1", "SystemApp2"],
                "path": "/path/to/system/apps",
            }
        }

        util.open_apps("system")

        expected_calls = [
            call("/path/to/system/apps", "SystemApp1"),
            call("/path/to/system/apps", "SystemApp2"),
        ]
        mock_open_app.assert_has_calls(expected_calls)

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            util.open_apps("invalid_type")


class TestSortFilesBy(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory with sample files for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = self.temp_dir.name

        # Create some sample files in the temporary directory
        sample_files = ["z-file.txt", "c-file.mp3", "b-file.mp3", "a-file.mp3"]
        for file_name in sample_files:
            file_path = Path(self.temp_dir_path) / file_name
            file_path.touch()

    def test_sort_by_name_all_files(self):
        sorted_files = util.sort_files_by(self.temp_dir_path, "all", "name")
        expected_files = sorted(
            [
                Path(self.temp_dir_path) / "a-file.mp3",
                Path(self.temp_dir_path) / "b-file.mp3",
                Path(self.temp_dir_path) / "c-file.mp3",
                Path(self.temp_dir_path) / "z-file.txt",
            ]
        )
        self.assertEqual(sorted_files, expected_files)

    def test_sort_by_date_all_files(self):
        sorted_files = util.sort_files_by(self.temp_dir_path, "all", "date")
        self.assertEqual(
            sorted_files, sorted(sorted_files, key=lambda f: f.stat().st_ctime)
        )

    def test_sort_by_name_mp3_files(self):
        sorted_files = util.sort_files_by(self.temp_dir_path, "mp3", "name")
        expected_files = sorted(
            [
                Path(self.temp_dir_path) / "c-file.mp3",
                Path(self.temp_dir_path) / "b-file.mp3",
                Path(self.temp_dir_path) / "a-file.mp3",
            ]
        )
        self.assertEqual(sorted_files, expected_files)

    def test_sort_by_date_mp3_files(self):
        sorted_files = util.sort_files_by(self.temp_dir_path, "mp3", "date")
        self.assertEqual(
            sorted_files, sorted(sorted_files, key=lambda f: f.stat().st_ctime)
        )

    def tearDown(self):
        self.temp_dir.cleanup()


class TestYtDlpDownload(unittest.TestCase):
    def setUp(self):
        self.yt_url = "https://youtube.com/some_video_url"

    @patch("cm_util.util.get_yt_dl_options")
    @patch("yt_dlp.YoutubeDL")
    def test_download_mp3(self, mock_YoutubeDL, mock_get_options):
        # Mock the options to avoid yt_dlp.parse_options issues
        mock_get_options.return_value = {
            "format": "bestaudio/best",
            "ignoreerrors": True,
            "outtmpl": "%(title)s.%(ext)s",
        }

        # Mock the YoutubeDL instance and its download method
        ydl_instance = MagicMock()
        ydl_instance.download.return_value = 0
        mock_YoutubeDL.return_value.__enter__.return_value = ydl_instance

        url = self.yt_url
        media_company = "youtube"
        media_type = "mp3"

        util.yt_dlp_download(url, media_company, media_type)

        ydl_instance.download.assert_called_once_with([url])
        mock_get_options.assert_called_once_with(media_type)

    @patch("yt_dlp.YoutubeDL")
    def test_download_video(self, mock_YoutubeDL):
        # Mock the clean_url function
        url = self.yt_url

        # Mock the YoutubeDL instance and its download method
        ydl_instance = MagicMock()
        ydl_instance.download.return_value = 0
        mock_YoutubeDL.return_value.__enter__.return_value = ydl_instance

        media_company = "youtube"
        media_type = "video"

        util.yt_dlp_download(url, media_company, media_type)

        ydl_instance.download.assert_called_once_with([url])

    @patch("yt_dlp.YoutubeDL")
    def test_download_error(self, mock_YoutubeDL):
        url = "invalid-url"
        ydl_instance = MagicMock()
        # Mock download to raise an exception
        ydl_instance.download.side_effect = Exception("Download failed")
        mock_YoutubeDL.return_value.__enter__.return_value = ydl_instance

        media_company = "youtube"
        media_type = "video"

        with self.assertRaises(Exception) as cm:
            util.yt_dlp_download(url, media_company, media_type)

        self.assertIn("Download failed", str(cm.exception))

    @patch("cm_util.util.get_yt_dl_options")
    @patch("yt_dlp.YoutubeDL")
    def test_download_non_zero_error_code(self, mock_YoutubeDL, mock_get_options):
        """Test that non-zero error codes from yt-dlp are handled correctly"""
        # Mock the options to avoid yt_dlp.parse_options issues
        mock_get_options.return_value = {
            "format": "bestaudio/best",
            "ignoreerrors": True,
            "outtmpl": "%(title)s.%(ext)s",
        }

        url = "https://youtube.com/some_video"
        ydl_instance = MagicMock()
        # Mock download to return non-zero error code
        ydl_instance.download.return_value = 1
        mock_YoutubeDL.return_value.__enter__.return_value = ydl_instance

        media_company = "youtube"
        media_type = "mp3"

        with self.assertRaises(Exception) as cm:
            util.yt_dlp_download(url, media_company, media_type)

        self.assertIn("error code: 1", str(cm.exception).lower())


class TestMoveMp3FilesToItunes(unittest.TestCase):

    def test_move_mp3_files_to_music_folder(self):
        """Test moving mp3 files to itunes music folder"""
        util.move_mp3_files_to_music_folder = MagicMock()
        util.move_mp3_files_to_music_folder()
        util.move_mp3_files_to_music_folder.assert_called_once()

    def test_itunes_music_folder_not_exist(self):
        with self.assertRaises(ValueError) as cm:
            util.move_mp3_files_to_music_folder("invalid_path")
        self.assertEqual(
          "Path invalid_path does not exist",
          str(cm.exception)
        )


if __name__ == "__main__":
    unittest.main()
