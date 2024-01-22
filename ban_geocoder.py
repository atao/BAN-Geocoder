#!/usr/bin/python
# -*- coding: utf-8 -*

import sys
from geocoder.cli import cli

if __name__ == '__main__':
    if len(sys.argv) == 1:
        cli.main(['--help'])
    else:
        cli()
