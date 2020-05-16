import json
import csv
import time

jsondata = []
modes = ['walk', 'bicycle', 'bus-metro', 'drive']
with open('../../data/trip-mode.csv','r') as datafile:
    csvdata = csv.reader(datafile)

    firstflag = True
    imsi = ""
    mode = ""
    coords = []
    for line in csvdata:
        if(firstflag):
            firstflag = False
            continue
        if(line[5] == 'T'):
            if(line[2] == imsi and line[6] == mode):
                coords.append([float(line[3]), float(line[4])])
                jsondata.append({'imsi':imsi, 'mode':modes[int(mode)-1], 'coords':coords})
            else:
                imsi = line[2]
                mode = line[6]
                coords = []
                coords.append([float(line[3]), float(line[4])])
        else:
            coords.append([float(line[3]), float(line[4])])
    datafile.close()

with open('../../data/trip-mode-data.json', 'w+') as jsonfile:
    json.dump(jsondata, jsonfile)
    jsonfile.close()

print(jsondata)
