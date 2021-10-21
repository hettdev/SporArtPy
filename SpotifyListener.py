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

def getTrackId(playback):
    return playback['item']['id']

def getAlbumArtUrl(playback):
    return next(image for image in playback['item']['album']['images'] if image['height'] == 64)['url']

def getAlbumArt(playback):
    url = getAlbumArtUrl(playback)
    content = requests.get(url, stream=True).content
    image = Image.open(io.BytesIO(content))
    return image

def saveImage(image):
    image.save("albumart.jpg")

def screensaver():
    os.system('./send-image -h localhost:1337 -g 64x64 snorlax.png')

spotify = getSpotifyAuth()

showingNothing = False

while True:
    try:
        playback = spotify.current_playback()
        if(playback==None):
            print("nothing is playing")
            if(showingNothing == False):
                showingNothing=True
                screensaver()
        else:
            showingNothing=False
            id = getTrackId(playback)
            if id != lastPlayedTrack:
                plt.draw()
                lastPlayedTrack = id
                trackName = getTrackName(playback)
                artist = getArtistName(playback)
                print(f"currently playing: {trackName} by {artist}")
                image = getAlbumArt(playback)
                saveImage(image)
                try:
                    os.system('./send-image -h localhost:1337 -g 64x64 albumart.jpg')
                except:
                    print("send-image not available, is flaschen-taschen installed?")
    except BaseException:
        screensaver()
    time.sleep(1)