# coding: utf-8

import json
import argparse
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


# Find the next trip in the stream of data
def index_gap(l, gap):
    # print "Find next GAP -> "+str(gap)
    rv = -1
    for i in range(0, len(l) - 2):
        time = l[i + 1]['timestamp'][0] - l[i]['timestamp'][0]
        if time >= gap:
            # print "GAP -> "+str(time)
            rv = i + 1
            break
    return rv


# Remove the extremes of the list
def discard_points(l, skip):
    if len(l) > 1:
        begin = l[0]['timestamp'][0]
        end = l[-1]['timestamp'][0]
        # discard top elements
        index = -1
        for i in range(0, len(l)):
            time = l[i]['timestamp'][0] - begin
            if time >= skip:
                index = i
                break
        if index > -1:
            l = l[index:]
        else:
            l = []
        # discard bottom elements
        index = -1
        for i in range(len(l) - 1, -1, -1):
            time = end - l[i]['timestamp'][0]
            if time >= skip:
                index = i
                break
        if index > -1:
            l = l[:index]
        else:
            l = []
    else:
        l = []
    return l


# Giving a stream of points, split them into different trips
def stream2trips(l, gap, skip):
    rv = []
    index = index_gap(l, gap)
    while index > -1:
        trip = l[:index]
        l = l[index:]
        rv.extend(discard_points(trip, skip))
        index = index_gap(l, gap)
    return rv


def main(args):
    gap = args.gap * 60000
    skip = args.skip * 60000
    for f in args.files:
        print('Processing file: '+f)
        j = json.load(f)
        dataset = j['dataset']
        cache = {}
        map_ids = []
        # load dataset to a single dict
        for element in dataset:
            if element['id'] not in map_ids:
                map_ids.append(element['id'])
            uid = map_ids.index(element['id'])
            element['id'] = uid

            if uid in cache:
                cache[uid].append(element)
            else:
                cache[uid] = [element]

        # For each sensor split stream into trips
        dataset = []
        for uid in cache:
            l = cache[uid]
            # Sort stream of points
            l.sort(key=lambda element: element['timestamp'][0])
            # Split points into trips and remove the extremes
            dataset.extend(stream2trips(l, gap, skip))
        with open(splitext(f.name)[0]+'.anon.json', 'w') as out:
            json.dump({'dataset': dataset}, out)
        print('Anonymize file: '+splitext(f.name)[0]+'.anon.json')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Road Dataset Anonymization')
    parser.add_argument('files', nargs='+', type=argparse.FileType('r'), help='files to process')
    parser.add_argument('--gap',  type=check_positive, dest='gap',  default=3,
                        help='minimum gap between two trips (in minutes)')
    parser.add_argument('--skip', type=check_positive, dest='skip', default=1,
                        help='the amount of events to be discarded (in minutes)')
    args = parser.parse_args()
    main(args)
