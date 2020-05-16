import json
import csv
import time

jsondata = {}
with open('../../data/original-destination-data-v3.csv','r') as datafile:
    csvdata = csv.reader(datafile)

    firstflag = True
    for line in csvdata:
        if(firstflag):
            firstflag = False
            continue
        stime = str(line[0])
        etime = str(line[1])
        stimestr = stime[0:4]+'-'+stime[4:6]+'-'+stime[6:8]+' '+stime[8:10]+':'+stime[10:12]+':'+stime[12:14]
        etimestr = etime[0:4]+'-'+etime[4:6]+'-'+etime[6:8]+' '+etime[8:10]+':'+etime[10:12]+':'+etime[12:14]
        # starttime = time.mktime(time.strptime(stimestr, '%Y-%m-%d %H:%M:%S'))
        # endtime = time.mktime(time.strptime(etimestr, '%Y-%m-%d %H:%M:%S'))
        if str(line[2]) not in jsondata:
            jsondata[str(line[2])] = [{'starttime':stimestr, 'endtime':etimestr, 'coord':[float(line[3]), float(line[4])]}]
        else:
            aperson = jsondata[str(line[2])]
            #apoint = {}
            aperson.append({'starttime':stimestr, 'endtime':etimestr, 'coord':[float(line[3]), float(line[4])]})
    datafile.close()

with open('../../data/OD-json-data.json', 'w+') as jsonfile:
    json.dump(jsondata, jsonfile)
    jsonfile.close()

print(jsondata)
