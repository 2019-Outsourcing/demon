import json
import csv
import time
import array

finaldata = {}
jsondata = []
csvdata = []
for a in range(0,24):
    jsondata.insert(a,{})

basedate = '2018-10-03 00:00:00'
basetime = time.mktime(time.strptime(basedate, '%Y-%m-%d %H:%M:%S'))

with open('../../data/cleaned-signaling-data.csv','r') as datafile:
    csvdata = csv.reader(datafile)

    firstflag = True
    for line in csvdata:
        #print(line)
        if(firstflag):
            firstflag = False
            continue
        atime = str(line[0])
        timestr = atime[0:4]+'-'+atime[4:6]+'-'+atime[6:8]+' '+atime[8:10]+':'+atime[10:12]+':'+atime[12:14]
        #print(timestr)
        recordtime = time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S'))
        index = 0
        while (basetime+index*60*60) < recordtime:
            # print(str(basetime+index*60*60) + '   ' + str(recordtime) + '    '+str(index))
            index += 1
        index -= 1
        # print(index)
        ahourrecord = jsondata.pop(index)
        recordkey = str(line[4])+'-'+str(line[5])
        if recordkey not in ahourrecord:
            ahourrecord[recordkey] = 1
        else:
            lodvalue = ahourrecord[recordkey]
            ahourrecord[recordkey] = lodvalue + 1
        jsondata.insert(index, ahourrecord)

    datafile.close()

for indexs in range(0,24):
    records = jsondata.pop(0)
    ahour = []
    for key,value in records.items():
        coord = key.split('-')
        coord[0] = float(coord[0])
        coord[1] = float(coord[1])
        arecord = {}
        arecord['coord'] = coord
        arecord['elevation'] = value
        ahour.append(arecord)
    recordtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(basetime+indexs*60*60))
    finaldata[recordtime] = ahour

with   open('../../data/thermal-chart-data.json', 'w') as jsonfile:
    json.dump(finaldata, jsonfile)
    jsonfile.close()

print(finaldata)
