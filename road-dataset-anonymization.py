import json
import argparse
import random
import string
from os.path import splitext
# import pprint


def random_id(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


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


def discard_points(l, skip):
    if len(l) > 1:
        begin = l[0]['timestamp'][0]
        end = l[-1]['timestamp'][0]
        print('Discard points -> (' + str(len(l)) + '; ' + str(begin) + '; ' + str(end) + '; ' + str(skip) + ')')
        # discard top elements
        index = -1
        for i in range(0, len(l)):
            time = l[i]['timestamp'][0] - begin
            if time >= skip:
                # print 'Time: ' + str(time)
                index = i
                break
        # print 'Begin Index: '+str(index)
        if index > -1:
            l = l[index:]
        else:
            l = []
        # print 'List without top: ' + str(len(l))
        # discard bottom elements
        index = -1
        for i in range(len(l) - 1, -1, -1):
            time = end - l[i]['timestamp'][0]
            # print 'Time: ' + str(time)
            if time >= skip:
                # print 'Time: ' + str(time)
                index = i
                break
        # print 'End Index: '+str(index)
        if index > -1:
            l = l[:index]
        else:
            l = []
        print('Final list: '+str(len(l)))
    else:
        l = []
    return l


def main(args):
    # pp = pprint.PrettyPrinter(indent=2)
    gap = args.gap * 60000
    skip = args.skip * 60000
    # print 'GAP: '+str(gap)+' SKIP: '+str(skip)
    for f in args.files:
        j = json.load(f)
        dataset = j['data']
        cache = {}
        # load dataset to a single dict
        for element in dataset:
            sensor_id = element['id']
            new_id = random_id(15)
            if sensor_id in cache:
                new_id = cache[sensor_id]
            else:
                cache[sensor_id] = new_id
            element['id'] = new_id

        dataset.sort(key=lambda element: element['timestamp'][0])
        print('Final trips sorted...')
        with open(splitext(f.name)[0]+'.anon.json', 'w') as out:
            json.dump({'dataset': j}, out, indent=2)
        print('JSON dump...')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Road Dataset Anonymization')
    parser.add_argument('files', nargs='+', type=argparse.FileType('r'), help='files to process')
    parser.add_argument('--gap',  type=check_positive, dest='gap',  default=2,
                        help='minimum gap between two trips (in minutes)')
    parser.add_argument('--skip', type=check_positive, dest='skip', default=2,
                        help='the amount of events to be discarded (in minutes)')
    args = parser.parse_args()
    main(args)
    # sys.exit(0)
