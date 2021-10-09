import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os.path
import time

redirectUrl = "https://example.com/callback"
secrets = "secrets.json"

# Either load clientsecret from file, or (if not existent) ask user for input
if os.path.isfile(secrets):                # check if file exists
    with open(secrets) as openedFile:      # open file as 'openedFile'
        data = json.load(openedFile)        # load as dict (json)
        clientId = data['name']             # get clientId fron dict
        clientSecret = data['secret']       # get clientData from dict
else:
    clientId = input("enter client id: ")               # get userinput for clientId
    clientSecret = input("enter user secret: ")         # get userinput for clientSecret
    secrets = {"name":clientId, "secret":clientSecret}  # create dictionary with values
    with open(secrets, "w") as jsonFile:               # open file as json_file
        json.dump(secrets, jsonFile)                    # save dictionary in file

# permissions the app needs
# user-read-playback-state: for reading what song is currently playing
scope = "user-read-playback-state" 

# create spotify object
# will open browser window for authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope, 
        client_id=clientId, 
        client_secret=clientSecret, 
        redirect_uri=redirectUrl))


