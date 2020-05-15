import json
import csv
import time

jsondata = {}
with open('../../data/cleaned-signaling-data.csv','r') as datafile:
    csvdata = csv.reader(datafile)

    firstflag = True
    for line in csvdata:
        if(firstflag):
            firstflag = False
            continue
        atime = str(line[0])
        timestr = atime[0:4]+'-'+atime[4:6]+'-'+atime[6:8]+' '+atime[8:10]+':'+atime[10:12]+':'+atime[12:14]
        #recordtime = time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S'))
        if str(line[1]) not in jsondata:
            jsondata[str(line[1])] = [{'time':timestr, 'coord':[float(line[4]), float(line[5])]}]
        else:
            aperson = jsondata[str(line[1])]
            #apoint = {}
            aperson.append({'time':timestr, 'coord':[float(line[4]), float(line[5])]})
    datafile.close()

with   open('../../data/person-travel-data.json', 'w') as jsonfile:
    json.dump(jsondata, jsonfile)
    jsonfile.close()

print(jsondata)