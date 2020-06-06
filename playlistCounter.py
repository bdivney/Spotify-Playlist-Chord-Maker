import json
from chord import Chord
import numpy as np


with open('DivsResults') as json_file:
    data = json.load(json_file)
    names = data["playlists"]
    toScan = data["items"]

ph = {}
for pl in names:
    ph[pl] = names.index(pl)

matrix = np.zeros((len(names), len(names)), dtype = int)
#matrix[1,0] = 1


for playlist in names:
    for entry in toScan:
        if toScan[entry]["count"] < 2:
            continue
        if playlist not in toScan[entry]["appearsIn"]:
            continue
        
        
        for otherPlaylist in toScan[entry]["appearsIn"]:
            if otherPlaylist == playlist:
                continue
            
            matrix[ph[playlist], ph[otherPlaylist]] = matrix[ph[playlist], ph[otherPlaylist]] + 1
        
    
    
    
    
    
    



m = matrix.tolist()
print(m)
Chord(m, names, wrap_labels=False, padding=0.01, width=900).to_html()
