# Road Dataset Utilities

Set of utilities to manipulate the [road dataset](https://atnog.av.it.pt/~mantunes/road/index.html).

All the utilities were written in Python 2.

## Prerequisites

As stated the utilities were written in Python 2.

Most of the code can run using Python 3, however the pykml library does not work with Python 3. 

For the full list of requirements see [requirements.txt](requirements.txt)

The requirements can be installed with pip:
```
pip install -r requirements.txt
```

## Utilities

1. **road-dataset-anonymization:** tool used to anonimize the original dataset into a new one.
It identifies trips, removes the extremes and changes the identifiers of each sensor.

2. **json2kml:** tool that converts a road dataset into multiple KML files contains the points of a single sensor id.

3. **json2csv:** tool that converts a road dataset into a CSV dataset.
The tool automatically compresses or expands the accelerations values in order to match the desired number of samples. 

## Authors

* **[Mário Antunes](https://github.com/mariolpantunes)**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.