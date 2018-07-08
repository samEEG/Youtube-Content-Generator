#!/usr/bin/python

# Usage example:
# python comments.py --videoid='<video_id>' --text='<text>'

import httplib2
import os
import sys

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains

# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  # Trusted testers can download this discovery document from the developers page
  # and it should be in the same directory with the code.
  with open("youtube-v3-discoverydocument.json", "r", encoding="utf8") as f:
    doc = f.read()
    return build_from_document(doc, http=credentials.authorize(httplib2.Http()))


# Call the API's commentThreads.list method to list the existing comment threads.
def get_comment_threads(youtube, video_id):
  results = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    textFormat="plainText",
    maxResults=100
  ).execute()

  for item in results["items"]:
    comment = item["snippet"]["topLevelComment"]
    reply_count = item["snippet"]["totalReplyCount"]
    like_count = comment["snippet"]["likeCount"]
    author = comment["snippet"]["authorDisplayName"]
    text = comment["snippet"]["textDisplay"]
    print("Reply Count: {}	Like Count: {}	Comment by {}: {}".format(reply_count,like_count,author, text))

  return results["items"]


# Call the API's comments.list method to list the existing comment replies.
def get_comments(youtube, video_comment_threads): 
  for comment in video_comment_threads:   
     results = youtube.comments().list(
       part="snippet",
       parentId=comment["id"],
       textFormat="plainText"
     ).execute()

     for item in results["items"]:
       author = item["snippet"]["authorDisplayName"]
       text = item["snippet"]["textDisplay"]
       like_count = item["snippet"]["likeCount"]
       print("Like Count: {}	Comment by {}: {}".format(like_count,author, text))


  return results["items"]

def search_channel(youtube, channel_id):
	results = youtube.search().list(
		part="snippet",
		channelId=channel_id,
		maxResults=5,
		order="date"
	).execute()

	for item in results["items"]:
		print("Title: {}".format(item["snippet"]["title"]))



# User, Comment, replyCount, likeCount, Is_this_toplevel_comment?, 







if __name__ == "__main__":
  # The "videoid" option specifies the YouTube video ID that uniquely
  # identifies the video for which the comment will be inserted.
  argparser.add_argument("--videoid",
    help="Required; ID for video for which the comment will be inserted.")
  args = argparser.parse_args()

  if not args.videoid:
    exit("Please specify videoid using the --videoid= parameter.")

  youtube = get_authenticated_service(args)
  # All the available methods are used in sequence just for the sake of an example.
  try:
  	search_channel(youtube, args.videoid) 
    #video_comment_threads = get_comment_threads(youtube, args.videoid)
    #video_comments = get_comments(youtube, video_comment_threads)

  except HttpError:
    print("An HTTP error {} occurred:{}".format(e.resp.status, e.content))
  else:
    print("Inserted, listed, updated, moderated, marked and deleted comments.")