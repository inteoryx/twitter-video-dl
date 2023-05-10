import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.twitter_video_dl.login import TwitterLoginClient
import argparse

#this temp bearertoken can be changed by the token from main.js.
BEARER_TOKEN = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Test for Twiiter login")

    parser.add_argument(
        "-a",
        required=True,
        type=str,
        help="username, email or phone number.  e.g. +8613300000000")

    parser.add_argument("-p",
                        required=True,
                        type=str,
                        help="The password of the account")

    args = parser.parse_args()
    #proxy = {"http": "http://127.0.0.1:7890"}
    login_client = TwitterLoginClient(bear_token=BEARER_TOKEN)
    login_client.login(username=args.a, password=args.p)

    print(login_client.cookie)
    print(login_client.csrftoken)