# twitter-video-dl-for-sc

This project is based on the original code of the [inteoryx / twitter-video-dl](https://github.com/inteoryx/twitter-video-dl) project, which allows users to download Twitter videos as MP4 files using only Python and URLs without the need for API keys or ffmpeg. I forked this project for use in iOS Shortcuts applications.

## Demo (Shortcuts)

|One video per tweet|Mixing images and videos in one tweet|Mixing images and videos in a thread|
|:---:|:---:|:---:|
|<img src="./demo/demo1_v1_30fps_400x866.gif" width="80%">|<img src="./demo/demo2_v1_30fps_400x866.gif" width="80%">|<img src="./demo/demo3_v2_30fps_400x866.gif" width="80%">|
|[Original Tweet Link](https://twitter.com/i/status/1650829030609022981)|[Original Tweet Link](https://twitter.com/i/status/1650829418863136768)|[Original Tweet Link](https://twitter.com/i/status/1650829765040013320)|

## Usage

### For Shortcuts

> **Note**ℹ️:
> **Currently only Japanese language support is available.**  
> **It has been tested on iPhone and iPad, but not on Mac.**  
>
> **Warning**⚠️:
> **Be sure to review the notes, limitations, and comments in the comments when performing shortcuts.**  

1. Download [Shortcuts](https://apps.apple.com/us/app/shortcuts/id915249334) and [a-Shell](https://apps.apple.com/jp/app/a-shell/id1473805438) from the AppStore
2. Add Shortcut to save Twitter videos
   * twitter-video-dl-sc setup ([iCloud Link](https://www.icloud.com/shortcuts/bd16e0c04216423ca98a1bacbf866915))
   * twitter-video-dl-sc ([iCloud Link](https://www.icloud.com/shortcuts/20e82f767f354607a4ebfa84de3e45b0))
3. Run the ***twitter-video-dl-sc setup*** setup shortcut  
   * DL [git](https://github.com/holzschu/a-Shell-commands/releases/download/0.1/git) command from [
a-Shell-commands](https://github.com/holzschu/a-Shell-commands)
   * git clone [twitter-video-dl-for-sc](https://github.com/7rikazhexde/twitter-video-dl-for-sc) and setup (pip install -r requirements.txt (just the requests library)).  
4. Run the ***twitter-video-dl-sc*** from a Twitter share  
   * If you do not specify an output file name, the file name is after the user _ id in the URL.
   * Replace '/' with '-' in the file name and new line ith '_'.

## For Windows / Mac / Linux

> **Note**ℹ️:
> **[Partially the same as twitter-video-dl and depends on it.](https://github.com/inteoryx/twitter-video-dl)**  

1. Clone the repo and pip install -r requirements.txt (just the requests library)
2. See a video on twitter that you want to save.
3. Invoke the script, e.g.:

```bash
# File name specified
python twitter-video-dl-for-sc.py https://twitter.com/willowhalliwell/status/1452460936116244482 output_file_name 0
```

```bash
# Without file name
python twitter-video-dl-for-sc.py https://twitter.com/willowhalliwell/status/1452460936116244482 ""  
```

Done, now you should have an mp4 file of the highest bitrate version of that video available.

## Auto Retry Feature

> **Note**ℹ️:
> **[Same as twitter-video-dl and depends on it.](https://github.com/inteoryx/twitter-video-dl)**  

From time to time, every week or so, Twitter will add some new request parameters that they expect from callers asking for their content.  Twitter refers to these as "features" or "variables".  The twitter-video-dl script will try to detect when a new feature or variable has been added and automatically accommodate the new element.  This is not foolproof though.  It's possible the script will fail with an error message.  If it does, please open an issue (or send a PR).

## Other

> **Note**ℹ️:
> **[Same as twitter-video-dl and depends on it.](https://github.com/inteoryx/twitter-video-dl)**  

I have tested this with the 10 video files listed in test_videos.txt and it seems to work.  Highly possible there are other variants out there that this won't work for.  If you encounter such, please submit an issue and include the URL that doesn't work.  If the script doesn't work double check you have the URL right.
