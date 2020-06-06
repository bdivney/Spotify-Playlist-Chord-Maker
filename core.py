import requests
import urllib.parse
import json
import operator
import datetime
import base64

allSongs = {}
playlists = {}
urlAUTH = "https://accounts.spotify.com/api/token"
clientID = ""
clientSecret = ""
b64Encoded = base64.b64encode((clientID + ":" + clientSecret).encode("utf-8")) #need to encode to bytes for some reason
encodedToken = "Basic " + str(b64Encoded.decode("utf-8")) # then decode from bytes, super fun
dataAUTH = {"grant_type":"client_credentials"}
headersAUTH = {"Authorization": encodedToken}

responseAUTH = requests.post(urlAUTH, headers = headersAUTH, data = dataAUTH)
responseAUTHData = responseAUTH.json()
accessToken = responseAUTHData["access_token"]
tokenType = responseAUTHData["token_type"]


##########################
user = "1226455532"
##########################


finished = False
offsetTimPlaylists = 0
urlTimPlaylists = "https://api.spotify.com/v1/users/" + user + "/playlists?offset=" + str(offsetTimPlaylists) + "&?limit=50"
while not finished:
    headersTimPlaylists = {"Accept" : "application/json", "Authorization" : "Bearer " + accessToken, "Content-Type" : "application/json"}
    responseTimPlaylists = requests.get(url = urlTimPlaylists, headers = headersTimPlaylists)
    raw = responseTimPlaylists.json()
    if raw["next"]:
        urlTimPlaylists = raw["next"]
    else:
        finished = True
    for playlist in raw["items"]:
        playlists[playlist["name"]] = playlist["id"]

offset = 0

for item in playlists:
    finished2 = False
    urlTPS = "https://api.spotify.com/v1/playlists/" + playlists[item] + "/tracks"
    headersTimurlTPS = {"Accept" : "application/json", "Authorization" : "Bearer " + accessToken, "Content-Type" : "application/json"}
    while not finished2:
        responseTimurlTPS = requests.get(url = urlTPS, headers = headersTimurlTPS)
        rawTPS = responseTimurlTPS.json()
        if rawTPS["next"]:
            urlTPS = rawTPS["next"]
        else:
            finished2 = True

        for song in rawTPS["items"]:
            songName = song["track"]["name"]
            if(songName not in allSongs):
                allSongs[songName] = {
                    "count" : 1, 
                    "appearsIn" : []
                    }
                
                allSongs[songName]["appearsIn"].append(item)
            else:
                allSongs[songName]["count"] = allSongs[songName]["count"] + 1
                (allSongs[songName]["appearsIn"]).append(item)
ex = {}
ex["playlists"] = list(playlists.keys())
ex["items"] = allSongs
print(json.dumps(ex))

#sorted_d = dict(sorted(allSongs.items(), key=operator.itemgetter(1),reverse=True))
#print('Dictionary in descending order by value : ',json.dumps(sorted_d))

