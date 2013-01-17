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
__version__ = "0.2"
__author__ = "Xose Pérez"
__contact__ = "xose.perez@gmail.com"
__copyright__ = "Copyright (C) 2013 Xose Pérez"
__license__ = 'GPL v3'

import sys
import time
from datetime import datetime
import ctypes

from libs.Daemon import Daemon
from libs.Config import Config
from libs.Mosquitto import Mosquitto

from libs.CloudServices import CloudServiceFactory
from libs.services.Cosm import Cosm
from libs.services.Tempodb import TempoDB

CloudServiceFactory.register('cosm', Cosm)
CloudServiceFactory.register('tempodb', TempoDB)

class MQTT2Cloud(Daemon):
    """
    MQTT2Cloud daemon.
    Glues the different components together
    """

    debug = True
    mqtt = None

    services = {}
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

    def load_services(self, services):
        """
        Instantiates and caches all objects for the different services
        """
        for code, data in services.iteritems():
            self.services[code] = CloudServiceFactory(data['class'], data['configuration'])

    def load_topics(self, topics):
        """
        Loads the mapping from MQTT topics to different cloud storage services
        """
        self.topics = {}
        for topic, rows in topics.iteritems():
            if topic not in self.topics:
                self.topics[topic] = []
            if type(rows) is not list:
                rows = [rows]
            for row in rows:
                code, feed, stream = row.split(':', 3)
                if not self.services.has_key(code):
                    raise Exception('Unknown service code: %s' % code)
                self.topics[topic].append({'service': code, 'feed': feed, 'stream': stream})

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
                self.log("[DEBUG] Subscribing to %s" % topic)
                self.mqtt.subscribe(topic, 0)
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
        self.log("[INFO] Subscription with mid %s received." % mid)

    def mqtt_on_message(self, obj, msg):
        """
        Incoming message, publish to all defined services if there is a mapping match
        """
        rows = self.topics.get(msg.topic, None)
        try:
            message = ctypes.string_at(msg.payload, msg.payloadlen)
        except:
            message = msg.payload
        for row in rows:
            self.log("[DEBUG] Message routed from %s to %s:%s:%s = %s" % (msg.topic, row['service'], row['feed'], row['stream'], message))
            self.services[row['service']].push(row['feed'], row['stream'], message)

    def run(self):
        """
        Entry point, initiates components and loops forever...
        """
        self.log("[INFO] Starting " + __app__ + " v" + __version__)
        self.mqtt_connect()

        while True:
            self.mqtt.loop()

if __name__ == "__main__":

    config = Config('mqtt2cloud.yaml')

    manager = MQTT2Cloud(config.get('daemon', 'pidfile', '/tmp/mqtt2cloud.pid'))
    manager.stdout = config.get('daemon', 'stdout', '/dev/null')
    manager.stderr = config.get('daemon', 'stderr', '/dev/null')
    manager.debug = config.get('daemon', 'debug', False)

    mqtt = Mosquitto(config.get('mqtt', 'client_id'))
    mqtt.host = config.get('mqtt', 'host')
    mqtt.port = config.get('mqtt', 'port')
    mqtt.keepalive = config.get('mqtt', 'keepalive')
    mqtt.clean_session = config.get('mqtt', 'clean_session')
    mqtt.qos = config.get('mqtt', 'qos')
    mqtt.retain = config.get('mqtt', 'retain')
    mqtt.status_topic = config.get('mqtt', 'status_topic')
    mqtt.set_will = config.get('mqtt', 'set_will')
    manager.mqtt = mqtt

    manager.load_services(config.get('services', default=[]))
    manager.load_topics(config.get('topics', default=[]))

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            manager.start()
        elif 'stop' == sys.argv[1]:
            manager.stop()
        elif 'restart' == sys.argv[1]:
            manager.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

