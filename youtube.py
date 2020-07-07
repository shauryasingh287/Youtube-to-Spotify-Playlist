import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies
# the name of a file that contains
# client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This scope allows for full read/write
# access to the authenticated user's account
# and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
	flow = InstalledAppFlow.from_client_secrets_file(
						CLIENT_SECRETS_FILE, SCOPES)

	credentials = flow.run_console()
	return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)



def storeResponse(response,filename):
    out_file = open(filename, "w")
    y = json.dump(response , out_file, indent = 6)
    out_file.close()

def playlists_songs(client , id):
    request = client.playlistItems().list(
        part = "snippet,contentDetails",
        maxResults = 25,
        playlistId = id
    )
    response  = request.execute()
    return response

def get_playlistid(index):
	f = open("myfile.json", "r")
	data = json.loads(f.read())
	return data['items'][index]['id']

def get_playlisttitle(index):
	f = open("myfile.json", "r")
	data = json.loads(f.read())
	return data['items'][index]['snippet']['title']


def getSongs(response):
	song_arr=[]
	for i in response['items']:
		song_arr.append(i['snippet']['title'])
	return song_arr

def print_response(response):
	print(response)

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
    	for key, value in kwargs.items():
        	if value:
        		good_kwargs[key] = value
    return good_kwargs

def playlists_mine(client, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)
    response = client.playlists().list(**kwargs).execute()
    return response



if __name__ == '__main__':

# When running locally, disable OAuthlib's
# HTTPs verification. When
# running in production * do not *
# leave this option enabled.
   os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
   client = get_authenticated_service()


response = playlists_mine(client,
	part ='snippet, contentDetails',
	mine = True,
	maxResults = 10,
	onBehalfOfContentOwner ='',
	onBehalfOfContentOwnerChannel ='')

storeResponse(response , "myfile.json")
playlist_number = 1
id = get_playlistid(playlist_number)
title = get_playlisttitle(playlist_number)
songs_res = playlists_songs(client , id)
songarr = getSongs(songs_res)
storeResponse(songs_res ,   "playInfo.json")
