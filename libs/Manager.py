#! /usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

#   MQTT to Cloud
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

__app__ = "MQTT to Cloud"
__version__ = "0.3.1"
__author__ = "Xose Pérez"
__contact__ = "xose.perez@gmail.com"
__copyright__ = "Copyright (C) 2013 Xose Pérez"
__license__ = 'GPL v3'

import sys
import time
from datetime import datetime
import ctypes

from Daemon import Daemon

class Manager(Daemon):
    """
    MQTT2Cloud manager.
    Glues the different components together
    """

    debug = True
    mqtt = None
    service = None

    topics = {}

    def log(self, message):
        """
        Log method.
        TODO: replace with standard python logging facility
        """
        if self.debug:
            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
            sys.stdout.write("[%s] %s\n" % (timestamp, message))
            sys.stdout.flush()

    def load_topics(self, topics):
        """
        Loads the mappings from MQTT topics
        """
        self.topics = {}
        for topic, data in topics.iteritems():
            feed, stream = data.split('/', 2)
            self.topics[topic] = {'feed': feed, 'stream': stream}

    def cleanup(self):
        """
        Clean up connections and unbind ports
        """
        self.mqtt.disconnect()
        self.log("[INFO] Exiting")
        sys.exit()

    def mqtt_connect(self):
        """
        Initiate connection to MQTT broker and bind callback methods
        """
        self.mqtt.on_connect = self.mqtt_on_connect
        self.mqtt.on_disconnect = self.mqtt_on_disconnect
        self.mqtt.on_message = self.mqtt_on_message
        self.mqtt.on_subscribe = self.mqtt_on_subscribe
        self.mqtt.connect()

    def mqtt_on_connect(self, obj, result_code):
        """
        Callback when connection to the MQTT broker has succedeed or failed
        """
        if result_code == 0:
            self.log("[INFO] Connected to MQTT broker")
            self.mqtt.send_connected()
            for topic, data in self.topics.iteritems():
                rc, mid = self.mqtt.subscribe(topic, 0)
                self.log("[INFO] Subscription to %s sent with MID %d" % (topic, mid))
        else:
            self.stop()

    def mqtt_on_disconnect(self, obj, result_code):
        """
        Callback when disconnecting from the MQTT broker
        """
        if result_code != 0:
            time.sleep(3)
            self.mqtt_connect()

    def mqtt_on_subscribe(self, obj, mid, qos_list):
        """
        Callback when succeeded subscription
        """
        self.log("[INFO] Subscription for MID %s confirmed." % mid)

    def mqtt_on_message(self, obj, msg):
        """
        Incoming message, publish to the defined service if there is a mapping match
        """
        data = self.topics.get(msg.topic, None)
        if data:
            try:
                message = ctypes.string_at(msg.payload, msg.payloadlen)
            except:
                message = msg.payload
            self.log("[DEBUG] Message routed from %s to %s:%s = %s" % (msg.topic, data['feed'], data['stream'], message))
            try:
                self.service.push(data['feed'], data['stream'], message)
            except Exception as e:
                self.log("[ERROR] %s" % e)

    def run(self):
        """
        Entry point, initiates components and loops forever...
        """
        self.log("[INFO] Starting " + __app__ + " v" + __version__)
        if not self.mqtt:
            self.log("[ERROR] MQTT broker not defined")
            sys.exit(2)
        if not self.service:
            self.log("[ERROR] Cloud service not defined")
            sys.exit(2)

        self.mqtt_connect()

        while True:
            self.mqtt.loop()

