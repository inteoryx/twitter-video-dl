import requests
import json
import shutil
import argparse
import re

GUEST_TOKEN_ENDPOINT = "https://api.twitter.com/1.1/guest/activate.json"
STATUS_ENDPOINT      = "https://twitter.com/i/api/graphql/"

QUOTED_VALUE  = re.compile("[\"']([^\"']+)[\"']")
MP4_PART    = re.compile("/.+mp4|/.+m4s")
VIDEO_BASE  = "https://video.twimg.com"
CONTAINER_PATTERN = re.compile("['\"](http[^'\"]+&container=fmp4)")

def send_request(url, session_method, headers):
    response = session_method(url, headers=headers, stream=True)
    assert response.status_code == 200, f"Failed request to {url}.  {response.status_code}.  Please submit an issue including this information."
    result = [line.decode("utf-8") for line in response.iter_lines()]
    return "".join(result)


def search_json(j, target_key, result):
    if type(j) == dict:
        for key in j:
            if key == target_key:
                result.append(j[key])
                
            search_json(j[key], target_key, result)
        return result
        
    if type(j) == list:
        for item in j:
            search_json(item, target_key, result)
        
        return result
    
    return result


def merge_files(f1, f2):
    for line in f2:
        f1.write(line)
        
    return f1


def download_video_parts(parts, fname):
    result = open(fname, "wb")
    
    paths = []
    for part in parts:
        paths.extend(MP4_PART.findall(part))
        
    for path in paths:
        full_path = f"{VIDEO_BASE}{path}"
        resp = requests.get(full_path, stream = True)
        assert resp.status_code == 200, f"Failed requesting {full_path}.  Please try again or report this as an issue. {resp}"
        
        merge_files(result, resp.raw)
    
    return result

def download_video(video_url, file_name):

    video_ids = re.findall("status/([0-9]+)", video_url)

    assert len(video_ids) == 1, f"Did not understand your twitter URL.  Example: https://twitter.com/james_a_rob/status/1451958941886435329"
    video_id = video_ids[0]
    status_params = f"TweetDetail?variables=%7B%22focalTweetId%22%3A%22{video_id}%22%2C%22with_rux_injections%22%3Afalse%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Afalse%2C%22withTweetQuoteCount%22%3Atrue%2C%22withBirdwatchNotes%22%3Afalse%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withUserResults%22%3Atrue%2C%22withNftAvatar%22%3Afalse%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%7D"

    session = requests.Session()
    headers = {}

    # One of the js files from original url holds the bearer token and query id.
    container = send_request(video_url, session.get, headers)
    js_files  = re.findall("src=['\"]([^'\"()]*js)['\"]", container)


    bearer_token = None
    query_id = None
    # Search the javascript files for a bearer token and TweetDetail queryId
    for f in js_files:
        file_content = send_request(f, session.get, headers)
        bt = re.search('["\'](AAA[a-zA-Z0-9%-]+%[a-zA-Z0-9%-]+)["\']', file_content)
        
        ops = re.findall('\{queryId:"[a-zA-Z0-9_]+[^\}]+"', file_content)
        query_op = [op for op in ops if "TweetDetail" in op]

        if len(query_op) == 1:
            query_id = re.findall('queryId:"([^"]+)"', query_op[0])[0]
        
        if bt:
            bearer_token = bt.group(1)

    assert bearer_token, f"Did not find bearer token.  Are you sure you used the right URL? {video_url}"
    assert query_id, f"Did not find query id.  Are you sure you used the right twitter URL? {video_url}"

    headers['authorization'] =  f"Bearer {bearer_token}"

    guest_token_resp = send_request(GUEST_TOKEN_ENDPOINT, session.post, headers)
    guest_token = json.loads(guest_token_resp)['guest_token']
    assert guest_token, f"Did not find guest token.  Probably means the script is broken.  Please submit an issue.  Include this message in your issue: {video_url}"
    headers['x-guest-token'] = guest_token

    status_resp = send_request(f"{STATUS_ENDPOINT}{query_id}/{status_params}", session.get, headers)
    container_urls  = CONTAINER_PATTERN.findall(status_resp)
    assert container_urls, f"Did not find container URLs.  Probably means the script is broken.  Please submit an issue.  Include this message in your issue: {video_url}"

    video_containers = []
    for container in container_urls:
        video_details = send_request(container, session.get, headers)
        video_suffixes = re.findall("(/[a-zA-Z0-9_?\/\.]*=fmp4)", video_details)

        resolutions = []
        for vs in video_suffixes:
            resolution = re.findall("([0-9]+)x([0-9]+)", vs)[0]
            resolutions.append((vs, int(resolution[0]) * int(resolution[1])))
            resolutions.sort(key=lambda x: x[1])

        if len(resolutions) > 0:
            video_containers.append(resolutions[-1])

    video_containers = set(video_containers)
    assert video_containers, f"Did not find video container.  Probably means the script is broken.  Please submit an issue.  Include this message in your issue: {video_url}"

    for i, vc in enumerate(video_containers):
        download_video_parts(
        send_request(f"{VIDEO_BASE}{vc[0]}", session.get, headers).split("#"),
        f"{file_name}.mp4" if i == 0 else f"{file_name}-{i}.mp4"
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download a video from a twitter url and save it as a local mp4 file."
    )

    parser.add_argument(
        "twitter_url", 
        type=str, 
        help="Twitter URL to download.  e.g. https://twitter.com/GOTGTheGame/status/1451361961782906889"
    )

    parser.add_argument(
        "file_name",
        type=str,
        help="Save twitter video to this filename. e.g. twittervid.mp4"
    )

    args = parser.parse_args()
    
    download_video(args.twitter_url, args.file_name if args.file_name[-4:] != ".mp4" else args.file_name[:-4])