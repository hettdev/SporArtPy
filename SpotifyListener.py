import io
import os
import errno
from requests.api import options, request
import spotipy
from spotipy import cache_handler
from spotipy.oauth2 import SpotifyOAuth
import json
import os.path
import time
import requests
from PIL import Image
import matplotlib.pyplot as plt

lastPlayedTrack = ''

def getSpotifyAuth():
    redirectUrl = "https://example.com/callback"
    fileName = "./secrets.json"

    # Either load clientsecret from file, or (if not existent) ask user for input
    if os.path.isfile(fileName):                # check if file exists
        with open(fileName) as openedFile:      # open file as 'openedFile'
            data = json.load(openedFile)        # load as dict (json)
            clientId = data['name']             # get clientId fron dict
            clientSecret = data['secret']       # get clientData from dict
    else:
        clientId = input("enter client id: ")               # get userinput for clientId
        clientSecret = input("enter user secret: ")         # get userinput for clientSecret
        secrets = {"name":clientId, "secret":clientSecret}  # create dictionary with values
        with open(fileName, "w") as jsonFile:               # open file as json_file
            json.dump(secrets, jsonFile)                    # save dictionary in file

    # permissions the app needs
    scope = "streaming user-read-playback-state"

    # create spotify object
    # will open browser window for authentication
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            client_id=clientId,
            client_secret=clientSecret,
            redirect_uri=redirectUrl,
            open_browser=False,
            cache_path="./spotifyCache"))

def getTrackName(playback):
    return playback['item']['name']

def getArtistName(playback):
    return playback['item']['artists'][0]['name']

# get the spotify ID of the current track
def getTrackId(playback):
    return playback['item']['id']

# returns URL of image with the highest resolution
def getAlbumArtUrl(playback):
    return playback['item']['album']['images'].sort(key=lambda x:x["height"], reverse=True)[0]['url']   

# get image for the currently playing song
def getAlbumArt(playback):
    url = getAlbumArtUrl(playback)
    content = requests.get(url, stream=True).content
    image = Image.open(io.BytesIO(content))
    return image

# save image to disk
def saveImage(image):
    image.save("albumart.jpg")

# show screensaver
def screensaver():
    sendSavedImage("snorlax.png")

# send saved image to flaschen-taschen
# will fail if flaschen-taschen is not installed
def sendSavedImage(imageFileName):
    try:
        os.system('./send-image -h localhost:1337 -g 64x64 {imageFileName}')
    except:
        print("send-image not available, is flaschen-taschen installed?")

showScreensaver = True

# actual routine begins here
print("creating Spotify login")
spotify = getSpotifyAuth()
print("done creating Spotify login")
while True:
    try:
        playback = spotify.current_playback()
        if(playback == None):
            print("nothing is playing")
            if(showScreensaver == True):
                showScreensaver = False
                screensaver()
        else:
            showScreensaver=False
            id = getTrackId(playback)
            if id != lastPlayedTrack:
                lastPlayedTrack = id
                trackName = getTrackName(playback)
                artist = getArtistName(playback)
                print(f"currently playing: {trackName} by {artist}")
                image = getAlbumArt(playback)
                saveImage(image)
                sendSavedImage("albumart.jpg")
    except BaseException:
        screensaver()
    time.sleep(1)