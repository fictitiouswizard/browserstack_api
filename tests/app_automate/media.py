import unittest
import os
from bsapi.app_automate import MediaFile, MediaApi
from requests.exceptions import HTTPError


class TestMediaApi(unittest.TestCase):

    def test_upload_file(self):
        try:
            media_file_response = MediaApi.upload_file(f"{os.getcwd()}/media/green_tree_python.jpg", custom_id="python")
            self.assertEqual(media_file_response.custom_id, "python")
        except HTTPError as http_error:
            print(http_error.response.json()["error"])
            self.fail()

    def test_recent_files(self):
        media_files = MediaApi.recent_files()
        self.assertGreaterEqual(len(media_files), 1)

    def test_recent_group_media(self):
        media_files = MediaApi.recent_group_media()
        self.assertGreaterEqual(len(media_files), 1)

    def test_delete(self):
        media_files = MediaApi.recent_files()
        if len(media_files) > 0:
            for media_file in media_files:
                success = MediaApi.delete(media_file.media_id)
                self.assertTrue(success)
        else:
            self.fail("Media file missing?")


def test_suite_media_api():
    suite = unittest.TestSuite()

    suite.addTest(TestMediaApi("test_upload_file"))
    suite.addTest(TestMediaApi("test_recent_files"))
    suite.addTest(TestMediaApi("test_recent_group_media"))
    suite.addTest(TestMediaApi("test_delete"))

    return suite


class TestMedia(unittest.TestCase):

    def test_delete(self):
        media_upload_response = MediaApi.upload_file(f"{os.getcwd()}/media/green_tree_python.jpg", custom_id="python")
        media_file = MediaApi.recent_files(media_upload_response.custom_id)[0]
        success = media_file.delete()
        self.assertTrue(success)


def test_suite_media():
    suite = unittest.TestSuite()

    suite.addTest(TestMedia("test_delete"))

    return suite

