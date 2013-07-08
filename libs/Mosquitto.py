#! /usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

#   Copyright (C) 2012 by Xose Pérez
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
__copyright__ = "Copyright (C) 2012 Xose Pérez"
__license__ = 'GPL v3'

import sys
from mosquitto import Mosquitto as _Mosquitto

class Mosquitto(_Mosquitto):
    """
    Wrapper for the official Mosquitto client that allows injection and easy mocking
    """

    client_id = 'xbee2mqtt'
    host = 'localhost'
    port = 1883
    keepalive = 60
    clean_session = False
    qos = 0
    retain = False
    status_topic = '/service/xbee2mqtt/status'
    set_will = False

    def connect(self):
        """
        Connects to the Mosquitto broker with the pre-configured parameters
        """
        if self.set_will:
            self.will_set(self.status_topic, "0", self.qos, self.retain)
        _Mosquitto.connect(self, self.host, self.port, self.keepalive)

    def publish(self, topic, value):
        """
        Publishes a value to a given topic, uses pre-loaded values for QoS and retain
        """
        _Mosquitto.publish(self, topic, str(value), self.qos, self.retain)

    def send_connected(self):
        """
        Send connection notification
        """
        self.publish(self.status_topic, "1")


