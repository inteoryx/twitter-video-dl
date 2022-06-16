# twitter-video-dl
Download twitter videos as mp4 files without API key, ffmpeg, or anything but python and a url.

# Usage
1. Clone the repo and pip install -r requirements.txt (just the requests library)
2. See a video on twitter that you want to save.
3. Invoke the script, e.g.: python twitter-video-dl.py https://twitter.com/willowhalliwell/status/1452460936116244482 output_file_name

Done, now you should have an mp4 file of the highest bitrate version of that video available.

# Auto Retry Feature

From time to time, every week or so, Twitter will add some new request parameters that they expect from callers asking for their content.  Twitter refers to these as "features" or "variables".  The twitter-video-dl script will try to detect when a new feature or variable has been added and automatically accommodate the new element.  This is not foolproof though.  It's possible the script will fail with an error message.  If it does, please open an issue (or send a PR).

# Other

I have tested this with the 10 video files listed in test_videos.txt and it seems to work.  Highly possible there are other variants out there that this won't work for.  If you encounter such, please submit an issue and include the URL that doesn't work.  If the script doesn't work double check you have the URL right.
