#! /usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

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

__author__ = "Xose Pérez"
__contact__ = "xose.perez@gmail.com"
__copyright__ = "Copyright (C) 2013 Xose Pérez"
__license__ = 'GPL v3'

from tempodb import Client, DataPoint
from datetime import datetime
from CloudService import CloudService

class TempoDB(CloudService):
    """
    Tempo-db.com client
    """

    _databases = None
    _timeout = 5

    def __init__(self, databases, timeout = None):
        """
        Constructor, provide API Key and secrets for multiple databases
        """
        self._databases = databases
        if timeout:
            self._timeout = timeout

    def push(self, database, series, value):
        """
        Pushes a single value with current timestamp to the given database/series
        """
        try:
            db =  self._databases[database]
            client = Client(db['api_key'], db['api_secret'])
            data = [DataPoint(datetime.now(), float(value))]
            client.write_key(series, data)
            self.last_response = 'OK'
            return True
        except Exception as e:
            self.last_response = e
            return False
