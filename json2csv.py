# coding: utf-8

import json
import csv

__author__ = "Mário Antunes"
__email__ = "mario.antunes@av.it.pt"
__version__ = "1.0"


def average(list):
    if len(list) == 0:
        return 0
    else:
        return sum(list)/len(list)


def fix_acc_series(timestamps, acc, nsamples):
    currentsamples = len(timestamps)
    begin = timestamps[0]
    end = timestamps[currentsamples-1]
    inc = (end-begin) / nsamples
    #print('('+str(begin)+'; '+str(end)+'; '+str(inc)+')')
    if currentsamples < nsamples:
        newacc = [acc[0]]
        stb = 0
        ste = 1
        for i in range(1, nsamples):
            time = begin + (inc*i)
            while time > timestamps[stb + 1]:
                stb += 1
            while time > timestamps[ste]:
                ste += 1
            #print(str(i)+"-> ("+str(timestamps[stb])+';'+str(timestamps[ste])+')')

            x1 = timestamps[stb]
            x2 = timestamps[ste]
            y1 = acc[stb]
            y2 = acc[ste]
            m = (y1-y2) / (x1-x2)
            b = y1 - (m*x1)
            newacc.append(m*time+b)
        return newacc
    elif currentsamples > nsamples:
        bins = [[] for x in range(nsamples)]
        for i in range(currentsamples):
            if i == currentsamples - 1:
                idx = nsamples - 1
            else:
                idx = int((timestamps[i]-begin)/inc)

            if idx >= len(bins):
                idx = len(bins)-1
            if idx < 0:
                idx = 0
            #print("Timestamp: "+str(timestamps[i]))
            #print("IDX: "+str(idx))
            try:
                bins[idx].append(acc[i])
            except IndexError:
                print("ERROR: bad index value: "+str(idx))

        #print(bins)
        newacc = []
        for bin in bins:
            newacc.append(average(bin))
        return newacc
    else:
        return acc

filename = 'dataset02_2014'
timestamps = [100, 102, 104, 106, 108, 110]
#values = [1, 2, 3, 4, 5, 6]
#print(fix_acc_series(timestamps, values, 3))
#timestamps = [100, 104, 110]
#values = [1, 3, 6]
#print(fix_acc_series(timestamps, values, 6))

with open(filename+'.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['id', 'version', 'latitude', 'longitude', 'speed', 'begin', 'end']+['x']*25+['y']*25+['z']*25)
    with open(filename+'.json') as jsonfile:
        json = json.load(jsonfile)
        dataset = json['dataset']
        for datum in dataset:
            id = datum['id']
            version = datum['version']
            latitude = datum['latitude']
            longitude = datum['longitude']
            speed = datum['speed']
            timestamps = datum['timestamp']
            begin = timestamps[0]
            end = timestamps[len(timestamps)-1]
            x = datum['accelerometer']['x']
            y = datum['accelerometer']['y']
            z = datum['accelerometer']['z']
            fx = fix_acc_series(timestamps, x, 25)
            fy = fix_acc_series(timestamps, y, 25)
            fz = fix_acc_series(timestamps, z, 25)
            line = [id, version, latitude, longitude, speed, begin, end]
            line.extend(fx)
            line.extend(fy)
            line.extend(fz)
            spamwriter.writerow(line)
