#!/bin/bash

FOLDER=.venv

if [ $# -eq 0 ]; then
    ACTION='activate'
else
    ACTION=$1
fi

case "$ACTION" in

    "activate")
        . venv/bin/activate
        ;;

    "deactivate")
        deactivate
        ;;

    "setup")
        if [ ! -d $FOLDER ]; then
            virtualenv $FOLDER
        fi

        deactivate
        source $FOLDER/bin/activate

        pip install ConfigParser
        pip install pyaml
	pip install mosquitto
	pip install requests

        wget https://bitbucket.org/oojah/mosquitto/raw/v1.3/lib/python/mosquitto.py
        mv mosquitto.py $FOLDER/lib/python2.7/site-packages/

        ;;

    "start" | "stop" | "restart")
        source $FOLDER/bin/activate
        python mqtt2xively.py $ACTION
        #python mqtt2tempodb.py $ACTION
        python mqtt2thingspeak.py $ACTION
        #python mqtt2sense.py $ACTION
        python mqtt2thethingsio.py $ACTION
        deactivate
        ;;

    *)
        echo "Unknown action $ACTION."
        ;;
esac
