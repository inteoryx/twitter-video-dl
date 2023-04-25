# twitter-video-dl-for-sc
This project is based on the original code of the [inteoryx / twitter-video-dl](https://github.com/inteoryx/twitter-video-dl) project, which allows users to download Twitter videos as MP4 files using only Python and URLs without the need for API keys or ffmpeg. I forked this project for use in iOS Shortcuts applications.

# Usage
## For Shortcuts
Note:   
Currently only Japanese language support is available.  
It has been tested on iPhone and iPad, but not on Mac.

1. Download [Shortcuts](https://apps.apple.com/us/app/shortcuts/id915249334) and [a-Shell](https://apps.apple.com/jp/app/a-shell/id1473805438) from the AppStore
2. Add Shortcut to save Twitter videos
   * twitter-video-dl-sc setup ([iCloud Link](https://www.icloud.com/shortcuts/cbbf2f112c3f42a49f85e738be7d5c82))
   * twitter-video-dl-sc ([iCloud Link](https://www.icloud.com/shortcuts/20e82f767f354607a4ebfa84de3e45b0))

## For Windows / Mac / Linux
Note: [Partially the same as twitter-video-dl and depends on it.](https://github.com/inteoryx/twitter-video-dl)  
1. Clone the repo and pip install -r requirements.txt (just the requests library)
2. See a video on twitter that you want to save.
3. Invoke the script, e.g.: 
  * File name specified  
python twitter-video-dl-for-sc.py https://twitter.com/willowhalliwell/status/1452460936116244482 output_file_name 
  * Without file name  
python twitter-video-dl-for-sc.py https://twitter.com/willowhalliwell/status/1452460936116244482 ""  
  
Done, now you should have an mp4 file of the highest bitrate version of that video available.

# Auto Retry Feature
Note: [Same as twitter-video-dl and depends on it.](https://github.com/inteoryx/twitter-video-dl)  
From time to time, every week or so, Twitter will add some new request parameters that they expect from callers asking for their content.  Twitter refers to these as "features" or "variables".  The twitter-video-dl script will try to detect when a new feature or variable has been added and automatically accommodate the new element.  This is not foolproof though.  It's possible the script will fail with an error message.  If it does, please open an issue (or send a PR).

# Other
Note: [Same as twitter-video-dl and depends on it.](https://github.com/inteoryx/twitter-video-dl)  
I have tested this with the 10 video files listed in test_videos.txt and it seems to work.  Highly possible there are other variants out there that this won't work for.  If you encounter such, please submit an issue and include the URL that doesn't work.  If the script doesn't work double check you have the URL right.
