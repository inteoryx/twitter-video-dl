"""
Tests for the module.  Tests require ffmpeg to be installed.
ffmpeg is not listed as a dependency in the setup.py file because it is only required for the tests.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ffmpeg
import json
import unittest
from src.twitter_video_dl import twitter_video_dl as tvdl

class VideoDLTester(unittest.TestCase):

    TOLERANCE = 0.05
    VIDEO_LIST = "TestVideos.json"


    def test_download_videos_from_list(self):
        """
        Load the list of videos to test, download them, probe, and compare to expected values.
        """

        with open(self.VIDEO_LIST, "r") as f:
            videos_j = json.load(f)

        for video in videos_j["videos"]:
            print("Testing: ", video["url"])
            tvdl.download_video(video["url"], "test.mp4")

            # Probe the video to confirm we have downloaded it.
            probe = ffmpeg.probe("test.mp4")

            actual_duration = float(probe["format"]["duration"])
            actual_size = float(probe["format"]["size"])
            expected_duration = float(video["duration"])
            expected_size = float(video["size"])

            # Check duration and size are within tolerances.
            self.assertAlmostEqual(actual_duration, expected_duration, delta=(self.TOLERANCE * expected_duration))
            self.assertAlmostEqual(actual_size, expected_size, delta=(self.TOLERANCE * expected_size))

            os.remove("test.mp4")
            print("Passed: ", video["url"])

if __name__ == "__main__":
    unittest.main()