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

import requests
import json
from CloudService import CloudService

class Sense(CloudService):
    """
    Sense.com client
    """

    api_key = ''
    timeout = 5

    datapoints = []
    base_url = "http://api.sen.se/events/"

    def __init__(self, api_key, timeout = None):
        """
        Constructor, provide API Key
        """
        self.api_key = api_key
        if timeout:
            self.timeout = timeout

    def headers(self):
        return {
            'sense_key': self.api_key,
            'Content-type': 'application/json'

        }

    def push(self, feed, datastream, value):
        """
        Pushes a single value with current timestamp to the given feed
        """
        try:
    	    data = { 'feed_id': feed, 'value': value }
	        response = requests.post(self.base_url, data=json.dumps(data), headers=self.headers(), timeout=self.timeout)
    	    self.last_response = response.status_code
            return self.last_response == 200
        except Exception as e:
            self.last_response = e
            return False
