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
import time
from CloudService import CloudService

class Thingspeak(CloudService):
    """
    Thingspeak.com client
    """

    channels = {}
    api_url = "http://api.thingspeak.com/update"
    time_between_updates = 15

    def __init__(self, channels, group_fields=True, group_timeout=2, request_timeout=5):
        """
        Constructor, Api Key mandatory
        """
        for id, key in channels.iteritems():
            self.channels[id] = {
                'key': key,
                'timeout': None,
                'data': dict()
            }

        self.group_fields = group_fields
        self.group_timeout = group_timeout
        self.request_timeout = request_timeout

    def push(self, channel, field, value):
        """
        Pushes a single value with current timestamp to the given feed/datastream
        """
        channel = self.channels.get(channel)
        if channel == None:
            return False

        channel['data'][field] = value
        if self.group_fields:
            channel['timeout'] = max(channel['timeout'], time.time() + self.group_timeout)
        else:
            channel['timeout'] = max(channel['timeout'], time.time())

        return True

    def loop(self):
        """
        Continuously check for pending sendings
        """
        for id, channel in self.channels.iteritems():
            if channel['timeout'] is not None and channel['timeout'] < time.time():
                if len(channel['data']) > 0:
                    self.send(channel['key'], channel['data'])
                channel['timeout'] = time.time() + self.time_between_updates
                channel['data'] = {}

    def send(self, key, data):
        """
        Actually sends the data
        """
        data['key'] = key
        response = requests.post(self.api_url, data=data, timeout=self.request_timeout)
        return response.status_code == 200

