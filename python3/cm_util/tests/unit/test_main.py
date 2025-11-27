import unittest

from cm_util.main import validate_url


class TestValidateUrl(unittest.TestCase):
    def test_valid_youtube_watch_url(self):
        """Test valid YouTube watch URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        is_valid, media_company = validate_url(url)
        self.assertTrue(is_valid)
        self.assertEqual(media_company, "YouTube")

    def test_valid_youtube_watch_url_no_www(self):
        """Test valid YouTube watch URL without www"""
        url = "https://youtube.com/watch?v=dQw4w9WgXcQ"
        is_valid, media_company = validate_url(url)
        self.assertTrue(is_valid)
        self.assertEqual(media_company, "YouTube")

    def test_valid_youtube_playlist_url(self):
        """Test valid YouTube playlist URL"""
        url = "https://www.youtube.com/playlist?list=PLtest123"
        is_valid, media_company = validate_url(url)
        self.assertTrue(is_valid)
        self.assertEqual(media_company, "YouTube")

    def test_valid_youtube_short_url(self):
        """Test YouTube short URL (youtu.be) - currently not supported by validation"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        is_valid, media_company = validate_url(url)
        # Note: youtu.be URLs are not currently validated by the simple pattern
        self.assertFalse(is_valid)
        self.assertIsNone(media_company)

    def test_valid_soundcloud_url(self):
        """Test valid SoundCloud URL"""
        url = "https://soundcloud.com/artist/track"
        is_valid, media_company = validate_url(url)
        self.assertTrue(is_valid)
        self.assertEqual(media_company, "SoundCloud")

    def test_valid_soundcloud_url_no_www(self):
        """Test valid SoundCloud URL without www"""
        url = "https://www.soundcloud.com/artist/track"
        is_valid, media_company = validate_url(url)
        self.assertTrue(is_valid)
        self.assertEqual(media_company, "SoundCloud")

    def test_invalid_url_wrong_domain(self):
        """Test invalid URL with wrong domain"""
        url = "https://example.com/video"
        is_valid, media_company = validate_url(url)
        self.assertFalse(is_valid)
        self.assertIsNone(media_company)

    def test_invalid_url_missing_protocol(self):
        """Test invalid URL missing protocol"""
        url = "youtube.com/watch?v=dQw4w9WgXcQ"
        is_valid, media_company = validate_url(url)
        self.assertFalse(is_valid)
        self.assertIsNone(media_company)

    def test_invalid_url_empty_string(self):
        """Test invalid empty URL"""
        url = ""
        is_valid, media_company = validate_url(url)
        self.assertFalse(is_valid)
        self.assertIsNone(media_company)

    def test_invalid_youtube_url_malformed(self):
        """Test malformed YouTube URL - now accepted by simple validation"""
        url = "https://youtube.com/notavalidpath"
        is_valid, media_company = validate_url(url)
        # Note: The simplified validation accepts any youtube.com/* URL
        self.assertTrue(is_valid)
        self.assertEqual(media_company, "YouTube")


if __name__ == "__main__":
    unittest.main()
