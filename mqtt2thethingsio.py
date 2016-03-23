#! /usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

#   MQTT to Cloud
#   Copyright (C) 2016 by Xose Pérez
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
__author__ = "Xose Pérez"
__contact__ = "xose.perez@gmail.com"
__copyright__ = "Copyright (C) 2016 Xose Pérez"
__license__ = 'GPL v3'

import sys

from libs.Config import Config
from libs.Mosquitto import Mosquitto
from libs.Manager import Manager

from libs.services.TheThingsIO import TheThingsIO

if __name__ == "__main__":

    config = Config('config/mqtt2thethingsio.yaml')

    manager = Manager(config.get('daemon', 'pidfile', '/tmp/mqtt2cloud.pid'))
    manager.stdout = config.get('daemon', 'stdout', '/dev/null')
    manager.stderr = config.get('daemon', 'stderr', '/dev/null')
    manager.debug = config.get('daemon', 'debug', False)

    mqtt = Mosquitto(config.get('mqtt', 'client_id'))
    mqtt.host = config.get('mqtt', 'host')
    mqtt.port = config.get('mqtt', 'port')
    mqtt.keepalive = config.get('mqtt', 'keepalive')
    mqtt.clean_session = config.get('mqtt', 'clean_session')
    mqtt.qos = config.get('mqtt', 'qos', 0)
    mqtt.retain = config.get('mqtt', 'retain', True)
    mqtt.status_topic = config.get('mqtt', 'status_topic')
    mqtt.set_will = config.get('mqtt', 'set_will')
    manager.mqtt = mqtt

    thethingsio = TheThingsIO(
        config.get('thethingsio', 'things')
    )
    manager.service = thethingsio

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
