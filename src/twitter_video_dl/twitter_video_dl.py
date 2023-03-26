import requests
import json
import re
import urllib.parse
import os


"""

Hey, thanks for reading the comments.  I love you.

Here's how this works:
1. To download a video you need a Bearer Token and a guest token.  The guest token definitely expires and the Bearer Token could, though in practice I don't think it does.
2. Use the video id get both of those as if you were an unauthenticated browser.
3. Call "TweetDetails" graphql endpoint with your tokens.
4. TweetDetails response includes a 'variants' key which is a list of video urls and details.  Find the one with the highest bitrate (bigger is better, right?) and then just download that.
5. If it's broken, fix it yourself because I'm very slow.  Or, hey, let me know, but I might not reply for months.

"""

variables = {
    "with_rux_injections":False,
    "includePromotedContent":True,
    "withCommunity":True,
    "withQuickPromoteEligibilityTweetFields":True,
    "withBirdwatchNotes":True,
    "withDownvotePerspective":False,
    "withReactionsMetadata":False,
    "withReactionsPerspective":False,
    "withVoice":True,
    "withV2Timeline":True
}

features={
    "responsive_web_twitter_blue_verified_badge_is_enabled":True,
    "responsive_web_graphql_exclude_directive_enabled":True,
    "verified_phone_label_enabled":False,
    "responsive_web_graphql_timeline_navigation_enabled":True,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled":False,
    "tweetypie_unmention_optimization_enabled": True,    "responsive_web_twitter_blue_verified_badge_is_enabled":True,
    "vibe_api_enabled": False,    "responsive_web_twitter_blue_verified_badge_is_enabled":True,
    "responsive_web_edit_tweet_api_enabled": False,   "responsive_web_twitter_blue_verified_badge_is_enabled":True,
    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": False,    "responsive_web_twitter_blue_verified_badge_is_enabled":True,
    "view_counts_everywhere_api_enabled": True,   "responsive_web_twitter_blue_verified_badge_is_enabled":True,
    "longform_notetweets_consumption_enabled":True,
    "tweet_awards_web_tipping_enabled":False,
    "freedom_of_speech_not_reach_fetch_enabled":False,
    "standardized_nudges_misinfo": False,   "responsive_web_twitter_blue_verified_badge_is_enabled":True,
    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":False,
    "interactive_text_enabled": False,   "responsive_web_twitter_blue_verified_badge_is_enabled":True,
    "responsive_web_text_conversations_enabled":False,
    "longform_notetweets_richtext_consumption_enabled":False,
    "responsive_web_enhance_cards_enabled":False
}



def get_tokens(tweet_url):
    """
    Welcome to the world of getting a bearer token and guest id.

    1. If you request the twitter url for the tweet you'll get back a blank 'tweet not found' page.  In the browser, subsequent javascript calls will populate this page with data.  The blank page includes a script tag for a 'main.js' file that contains the bearer token.
    2. 'main.js' has a random string of numbers and letters in the filename.  We will request the tweet url, use a regex to find our unique main.js file, and then request that main.js file.
    3. The main.js file contains a bearer token.  We will extract that token and return it.  We can find the token by looking for a lot of A characters in a row.
    4. Now that we have the bearer token, how do we get the guest id?  Easy, we already have it.  Guest token, or 'gt' if you're a Twitter dev, is set as a response header from the original request to the tweet url.  We can just grab it from the response headers and return it.
    """
    
    html = requests.get(tweet_url)

    assert html.status_code == 200, f'Failed to get tweet page.  If you are using the correct Twitter URL this suggests a bug in the script.  Please open a GitHub issue and copy and paste this message.  Status code: {html.status_code}.  Tweet url: {tweet_url}'

    mainjs_url = re.findall(r'https://abs.twimg.com/responsive-web/client-web-legacy/main.[^\.]+.js', html.text)

    assert mainjs_url is not None and len(mainjs_url) > 0, f'Failed to find main.js file.  If you are using the correct Twitter URL this suggests a bug in the script.  Please open a GitHub issue and copy and paste this message.  Tweet url: {tweet_url}'
    
    mainjs_url = mainjs_url[0]

    mainjs = requests.get(mainjs_url)

    assert mainjs.status_code == 200, f'Failed to get main.js file.  If you are using the correct Twitter URL this suggests a bug in the script.  Please open a GitHub issue and copy and paste this message.  Status code: {mainjs.status_code}.  Tweet url: {tweet_url}'

    bearer_token = re.findall(r'AAAAAAAAA[^"]+', mainjs.text)

    assert bearer_token is not None and len(bearer_token) > 0, f'Failed to find bearer token.  If you are using the correct Twitter URL this suggests a bug in the script.  Please open a GitHub issue and copy and paste this message.  Tweet url: {tweet_url}, main.js url: {mainjs_url}'

    bearer_token = bearer_token[0]

    guest_token = html.cookies['gt']

    assert guest_token is not None, f'Failed to find guest token.  If you are using the correct Twitter URL this suggests a bug in the script.  Please open a GitHub issue and copy and paste this message.  Tweet url: {tweet_url}, main.js url: {mainjs_url}'

    return bearer_token, guest_token


def get_details_url(tweet_id, features, variables):
    # create a copy of variables - we don't want to modify the original
    variables = {**variables}
    variables['focalTweetId'] = tweet_id
    
    return f"https://twitter.com/i/api/graphql/wTXkouwCKcMNQtY-NcDgAA/TweetDetail?variables={urllib.parse.quote(json.dumps(variables))}&features={urllib.parse.quote(json.dumps(features))}"


def get_tweet_details(tweet_url, guest_token, bearer_token):
    tweet_id = re.findall(r'(?<=status/)\d+', tweet_url)

    assert tweet_id is not None and len(tweet_id) == 1, f'Could not parse tweet id from your url.  Make sure you are using the correct url.  If you are, then file a GitHub issue and copy and paste this message.  Tweet url: {tweet_url}'

    tweet_id = tweet_id[0]


    # the url needs a url encoded version of variables and features as a query string
    url = get_details_url(tweet_id, features, variables)

    details = requests.get(url, headers={
        'authorization': f'Bearer {bearer_token}',
        'x-guest-token': guest_token,
    })
    
    return details


def extract_mp4s(j):
    # pattern looks like https://video.twimg.com/amplify_video/1638969830442237953/vid/1080x1920/lXSFa54mAVp7KHim.mp4?tag=16 or https://video.twimg.com/ext_tw_video/1451958820348080133/pu/vid/720x1280/GddnMJ7KszCQQFvA.mp4?tag=12
    amplitude_pattern = re.compile(r'(https://video.twimg.com/amplify_video/(\d+)/vid/(\d+x\d+)/\w+.mp4\?tag=\d+)')
    ext_tw_pattern = re.compile(r'(https://video.twimg.com/ext_tw_video/(\d+)/pu/vid/(\d+x\d+)/\w+.mp4\?tag=\d+)')

    # https://video.twimg.com/ext_tw_video/1451958820348080133/pu/pl/b-CiC-gZClIwXgDz.m3u8?tag=12&container=fmp4
    container_pattern = re.compile(r'https://video.twimg.com/[^"]*container=fmp4')
    

    # find all the matches
    matches = amplitude_pattern.findall(j)
    matches += ext_tw_pattern.findall(j)

    container_matches = container_pattern.findall(j)
    if len(container_matches) > 0:
        return container_matches

    results = {}

    for match in matches:
        url, tweet_id, resolution = match
        if tweet_id not in results:
            results[tweet_id] = {'resolution': resolution, 'url': url}
        else:
            # if we already have a higher resolution video, then don't overwrite it
            my_dims = [int(x) for x in resolution.split('x')]
            their_dims = [int(x) for x in results[tweet_id]['resolution'].split('x')]

            if my_dims[0] * my_dims[1] > their_dims[0] * their_dims[1]:
                results[tweet_id] = {'resolution': resolution, 'url': url}



    return [x['url'] for x in results.values()]


def download_parts(url, output_filename):
    resp = requests.get(url, stream=True)
    
    # container begins with / ends with fmp4 and has a resolution in it we want to capture
    pattern = re.compile(r'(/[^\n]*/(\d+x\d+)/[^\n]*container=fmp4)')

    matches = pattern.findall(resp.text)

    max_res = 0
    max_res_url = None

    for match in matches:
        url, resolution = match
        width, height = resolution.split('x')
        res = int(width) * int(height)
        if res > max_res:
            max_res = res
            max_res_url = url

    assert max_res_url is not None, f'Could not find a url to download from.  Make sure you are using the correct url.  If you are, then file a GitHub issue and copy and paste this message.  Tweet url: {url}'

    video_part_prefix = "https://video.twimg.com"

    resp = requests.get(video_part_prefix + max_res_url, stream=True)

    mp4_pattern = re.compile(r'(/[^\n]*\.mp4)')
    mp4_parts = mp4_pattern.findall(resp.text)

    assert len(mp4_parts) == 1, f'There should be exactly 1 mp4 container at this point.  Instead, found {len(mp4_parts)}.  Please open a GitHub issue and copy and paste this message into it.  Tweet url: {url}'

    mp4_url = video_part_prefix + mp4_parts[0]

    m4s_part_pattern = re.compile(r'(/[^\n]*\.m4s)')
    m4s_parts = m4s_part_pattern.findall(resp.text)

    with open(output_filename, 'wb') as f:
        r = requests.get(mp4_url, stream=True)
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

        for part in m4s_parts:
            part_url = video_part_prefix + part
            r = requests.get(part_url, stream=True)
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

    return True


def download_video(tweet_url, output_file):
    bearer_token, guest_token = get_tokens(tweet_url)
    resp = get_tweet_details(tweet_url, guest_token, bearer_token)

    mp4s = extract_mp4s(resp.text)

    for mp4 in mp4s:
        if "container" in mp4:
            download_parts(mp4, output_file)
        else:
            # use a stream to download the file
            r = requests.get(mp4, stream=True)
            with open(output_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()


download_video("https://twitter.com/GOTGTheGame/status/1451361961782906889", "test.mp4")