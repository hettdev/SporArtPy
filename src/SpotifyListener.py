import io
import os
from os import listdir
from os.path import isfile, join
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os.path
import time
import requests
from PIL import Image
from datetime import datetime, timedelta
import random
import threading
import subprocess
import signal

# global variables
brightness = 78 # default brightness
random.seed(datetime.now().second)
#random.seed(4388)
secondsUntilNextScreensaverPicture = 3600
lastPlayedTrack = ''
screensaverCurrentlyShown = False
birghtnessServerUrl = "http://localhost:5000/api/brightness/"
threadLock = threading.Lock()
albumart = "albumart.jpg"
imageToShow = albumart
screensaverPath = "screenSaverPictures/gifs"
sendImageProcess = None

# functions
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
    sortedImages = sorted(playback['item']['album']['images'], key=lambda x:x["height"], reverse=True)
    return sortedImages[0]['url']

# get image for the currently playing song
def getAlbumArt(playback):
    url = getAlbumArtUrl(playback)
    content = requests.get(url, stream=True).content
    image = Image.open(io.BytesIO(content))
    return image

# save image to disk
def saveImage(image):
    threadLock.acquire()
    try:
        image.save("albumart.jpg")
    finally:
        threadLock.release()

timeStamp = datetime.now()
# show screensaver
def screensaver():
    currentTime = datetime.now()
    global timeStamp
    global imageToShow
    timeDifference = currentTime - timeStamp
    if timeDifference > timedelta(seconds=secondsUntilNextScreensaverPicture) or imageToShow == albumart:
        allFiles = [f for f in listdir(screensaverPath) if isfile(join(screensaverPath, f))]
        num = random.randint(0,len(allFiles)-1)
        timeStamp = currentTime
        #print(f"screensaverPictures/{num}.png")
        screensaverPicture = allFiles[num]
        imageToShow = f"{screensaverPath}/{screensaverPicture}"
        sendSavedImage()

# send saved image to flaschen-taschen
# will fail if flaschen-taschen is not installed
def sendSavedImage():
    threadLock.acquire()
    global sendImageProcess
    try:
        # os.system(f'./send-image -h localhost:1337 -g 64x64 {imageToShow} -b {brightness}')
        if(sendImageProcess != None):
            sendImageProcess.send_signal(signal.SIGINT)
        cmd = ['./send-image', '-h', 'localhost:1337', '-g', '64x64', imageToShow, '-b', str(brightness)]
        sendImageProcess = subprocess.Popen(args=cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(brightness)
    except BaseException as err:
        print("send-image not available, is flaschen-taschen installed?")
        print(err)
    finally:
        threadLock.release()

def getServerBrightness():
    try:
        req = requests.get(birghtnessServerUrl, timeout=3)
        if(req.status_code == 200):
            return req.content
    except:
        return brightness

def serverBrightnessThreadFunction():
    global brightness
    while True:
        newBrightness = int(getServerBrightness())
        if (newBrightness != brightness):
            brightness=newBrightness
            sendSavedImage()
        time.sleep(0.016)

# actual routine begins here
spotify = getSpotifyAuth()
brightnessThread = threading.Thread(target=serverBrightnessThreadFunction, daemon=True)
brightnessThread.start()
while True:
    try:
        playback = spotify.current_playback()
        if(playback == None):
            print(f"{datetime.now()}: nothing is playing")
            lastPlayedTrack = ''
            screensaver()
        else:
            screensaverCurrentlyShown = False
            id = getTrackId(playback)
            if id != lastPlayedTrack:
                lastPlayedTrack = id
                trackName = getTrackName(playback)
                artist = getArtistName(playback)
                print(f"currently playing: {trackName} by {artist}")
                image = getAlbumArt(playback)
                saveImage(image)
                imageToShow = albumart
                sendSavedImage()
    except BaseException as err:
        print(err)
        screensaver()
    time.sleep(1)