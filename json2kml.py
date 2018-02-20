# coding: utf-8

import argparse
import json
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from os.path import splitext

__author__ = "Mário Antunes"
__email__ = "mario.antunes@av.it.pt"
__version__ = "1.0"


def main(args):
    for f in args.files:
        trips = {}
        with open(f) as jfile:
            jdata = json.load(jfile)
            print('Load trips.')
            dataset = jdata['dataset']
            for point in dataset:
                #print(point)
                id = point['id']
                timestamp = point['timestamp'][0]
                lat = point['latitude']
                lon = point['longitude']
                if id in trips:
                    trips[id].append((timestamp, lat, lon))
                else:
                    trips[id] = [(timestamp, lat, lon)]
            print('Convert trips into KML files')
            for id in trips:
                trip = trips[id]
                single_trip = KML.kml(KML.Document())
                for trip_point in trip:
                    (timestamp, lat, lon) = trip_point
                    single_trip.Document.append(KML.Placemark(KML.Point(KML.coordinates(lat, lon))))
                with open(splitext(f.name)[0]+id+'.kml', "w") as text_file:
                    text_file.write(etree.tostring(single_trip, pretty_print=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='JSON 2 KML')
    parser.add_argument('files', nargs='+', type=argparse.FileType('r'), help='files to process')
    args = parser.parse_args()
    main(args)
