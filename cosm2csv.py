#! /usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

#   Cosm.com to CSV
#   Copyright (C) 2013 by Xose Pérez
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

__app__ = "Cosm.com to CSV"
__version__ = "0.1"
__author__ = "Xose Pérez"
__contact__ = "xose.perez@gmail.com"
__copyright__ = "Copyright (C) 2013 Xose Pérez"
__license__ = 'GPL v3'

import re
import datetime

from libs.services.Cosm import Cosm
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Cosm.com to CSV')
    parser.add_argument("-k", dest="api_key",  help="cosm.com API key", required=True)
    parser.add_argument("-f", dest="feed",  help="coms.com feed", required=True, type=int)
    parser.add_argument("-d", dest="datastream",  help="datastream in the feed", required=True)
    parser.add_argument("-s", dest="start",  help="start datetime (YYYY-MM-DD [HH:MM:SS])", required=True)
    parser.add_argument("-e", dest="end",  help="end datetime (YYYY-MM-DD [HH:MM:SS])", required=True)
    parser.add_argument("--format", dest="format",  help="output timestamp format")
    options = parser.parse_args()

    cosm = Cosm(options.api_key)

    start = datetime.datetime(*[int(x) for x in re.findall(r'\d+', options.start)])
    end = datetime.datetime(*[int(x) for x in re.findall(r'\d+', options.end)])

    print "timestamp,value"
    for ts, value in cosm.get(options.feed, options.datastream, start, end):
        if options.format:
            ts = datetime.datetime(*[int(x) for x in re.findall(r'\d+', ts)])
            ts = ts.strftime(options.format)
        print "%s,%s"  % (ts, value)

