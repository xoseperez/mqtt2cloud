# mqtt2cloud

This daemon will subscribe to an MQTT broker and push values to different providers whenever a message is recevied from certain topics.

## Requirements

* python-yaml
<pre>sudo apt-get install python-yaml</pre>

* python-mosquitto
<pre>sudo apt-get install python-mosquitto</pre>

* tempodb 
<pre>pip install tempodb</pre>

## Install

Just clone or extract the code in some folder. I'm not providing an setup.py file yet.

## Configuration

Rename or copy the mqtt2cloud.yaml.sample file to mqtt2cloud.yaml and edit it. The configuration is pretty straight forward:

### daemon

Just define the log file paths.

### mqtt

These are standard Mosquitto parameters. The status topic is the topic to post messages when the daemon starts or stops.

### services

List of cloud services. For every key you have to provide a class name (the same class name used when registering the CloudService class in the CloudServiceFactory) and the configuration parameters.
The configuration parameters are the same as in the cloud service constructor.

### topics

For every topic you want to push you have to specify a destination string. This destination string has three parameters, using ':' as separator:
- service key (see the services definition)
- feed / database
- datastream / series

If you only define one service per topic you can do it inline, otherwise list all the services:

<pre>
/raw/sensor/battery: cosm:45243:battery
</pre>

and

<pre>
/raw/sensor/battery: 
    - cosm:45243:battery
    - tempodb:sensor:battery
</pre>

## Running it

The util stays resident as a daemon. You can start it, stop it or restart it (to reload the configuration) by using:

<pre>python mqtt2cloud.py start|stop|restart</pre>



