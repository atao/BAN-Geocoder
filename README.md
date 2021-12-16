# Geocoder for adresse.data.gouv.fr
Geocoding addresses using the national address database API - [adresse.data.gouv.fr](https://adresse.data.gouv.fr/).

```
root@kali:~# python3 ban_geocoder.py -h
usage: ban_geocoder.py [-h] [-v] [-a ADDRESS] [--lat LAT] [--lon LON] [-s]
                       [-g] [--csv] [--version]

Geocoding addresses using the national address database API -
https://adresse.data.gouv.fr/ - BAN The data come from IGN, La Poste, DGFiP,
Etalab and OpenStreetMap France.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -a ADDRESS, --address ADDRESS
                        enter the address to geocoder
  -s, --score           show score
  -g, --gps             show coordinates
  --csv                 show all in csv format
  --version             show version

  --lat LAT, --latitude LAT
                        enter Latitude
  --lon LON, --longitude LON
                        enter Longitude
```

## Features
* Works on Windows and Linux
* Address spelling correction
* Address geocoding
* Reverse address geocoding
* Export to CSV format

## Requirements
* Python 3
* librarie :
  - requests (That can be installed using `pip install requests`)

## Examples
I want the coordinates of the Elysée and get the score :
```
root@kali:~# python3 ban_geocoder.py -a "55 rue Faubourg Saint-Honoré" --gps -s
55 Rue du Faubourg Saint-Honoré 75008 Paris
Coordinates : 2.31698, 48.870675
Score : 0.8598454545454546
```
Get the address corresponding to these coordinates and export to CSV :
```
root@kali:~# python3 ban_geocoder.py --lon 2.31698 --lat 48.870675 --csv
55 Rue du Faubourg Saint-Honoré 75008 Paris
55;Rue du Faubourg Saint-Honoré;75008;Paris;2.31698, 48.870675
```
