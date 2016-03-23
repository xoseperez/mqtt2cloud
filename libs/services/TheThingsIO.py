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
__copyright__ = "Copyright (C) 2016 Xose Pérez"
__license__ = 'GPL v3'

import requests
import json
import datetime
from CloudService import CloudService
from thethingsio.theThingsAPI import TheThingsAPI

class TheThingsIO(CloudService):
    """
    theThings.io client
    """

    things = None

    def __init__(self, things):
        """
        Constructor, provide API Key
        """
        self.things = things

    def push(self, thing, variable, value):
        """
        Pushes a single value with current timestamp to the given thing/variable
        """
        try:
            t = self.things.get(thing)
            api = TheThingsAPI(t['token'])
            api.addVar(variable, value)
            self.last_response = api.write()
            return self.last_response == 201
        except Exception as e:
            self.last_response = e
            return False
