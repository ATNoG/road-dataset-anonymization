# coding: utf-8

import argparse
import json
import csv
from os.path import splitext

__author__ = "Mário Antunes"
__email__ = "mario.antunes@av.it.pt"
__version__ = "1.0"


# Check if a int is a positive value
def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


# Computes the average of a list
def average(list):
    if len(list) == 0:
        return 0
    else:
        return sum(list)/len(list)


# Compress or expands a series of accelerations
def fix_acc_series(timestamps, acc, nsamples):
    current_samples = len(timestamps)
    begin = timestamps[0]
    end = timestamps[current_samples-1]
    inc = (end-begin) / nsamples
    if current_samples < nsamples:
        new_acc = [acc[0]]
        stb = 0
        ste = 1
        for i in range(1, nsamples):
            time = begin + (inc*i)
            while time > timestamps[stb + 1]:
                stb += 1
            while time > timestamps[ste]:
                ste += 1
            x1 = timestamps[stb]
            x2 = timestamps[ste]
            y1 = acc[stb]
            y2 = acc[ste]
            m = (y1-y2) / (x1-x2)
            b = y1 - (m*x1)
            new_acc.append(m*time+b)
        return new_acc
    elif current_samples > nsamples:
        bins = [[] for x in range(nsamples)]
        for i in range(current_samples):
            if i == current_samples - 1:
                idx = nsamples - 1
            else:
                idx = int((timestamps[i]-begin)/inc)
            if idx >= len(bins):
                idx = len(bins)-1
            if idx < 0:
                idx = 0
            try:
                bins[idx].append(acc[i])
            except IndexError:
                print("ERROR: bad index value: "+str(idx))
        new_acc = []
        for b in bins:
            new_acc.append(average(b))
        return new_acc
    else:
        return acc


def main(args):
    for f in args.files:
        with f as jsonfile, open(splitext(f.name)[0]+'.csv', 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['id', 'version', 'latitude', 'longitude', 'speed', 'begin', 'end']+['x']*args.ns+['y']*args.ns+['z']*args.ns)
            jfile = json.load(jsonfile)
            dataset = jfile['dataset']
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
                fx = fix_acc_series(timestamps, x, args.ns)
                fy = fix_acc_series(timestamps, y, args.ns)
                fz = fix_acc_series(timestamps, z, args.ns)
                line = [id, version, latitude, longitude, speed, begin, end]
                line.extend(fx)
                line.extend(fy)
                line.extend(fz)
                spamwriter.writerow(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='JSON 2 CSV')
    parser.add_argument('files', nargs='+', type=argparse.FileType('r'), help='files to process')
    parser.add_argument('--ns', type=check_positive, dest='ns', default=15, help='number of acceleration samples')
    args = parser.parse_args()
    main(args)
