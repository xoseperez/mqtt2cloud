# mqtt2cloud

MQTT2Cloud is a set of python daemons that will subscribe to an MQTT broker and push values to different providers whenever a message is recevied from certain topics.

## Requirements

* python-yaml
<pre>sudo apt-get install python-yaml</pre>

* python-mosquitto
<pre>sudo apt-get install python-mosquitto</pre>

* tempodb [if using TempoDB daemon]
<pre>pip install tempodb</pre>

* requests [tempodb installs this]
<pre>pip install requests</pre>

## Install

Just clone or extract the code in some folder. I'm not providing an setup.py file yet.

## Configuration

Rename or copy the config/mqtt2???.yaml.sample files to config/mqtt2???.yaml and edit them. The configuration is pretty straight forward:

### daemon

Just define the log file paths.

### mqtt

These are standard Mosquitto parameters. The status topic is the topic to post messages when the daemon starts or stops.

### cosm, xively, sen.se

The API key and timeout value.

### tempodb

A set of databases, each with its api key and secret.

### topics

For every topic you want to push you have to specify a destination string. This destination string has two parameters, using '/' as separator. 
Depending on the cloud service you are using these parameters could be: feed/datastream for xively.com, feed/(empty) for sen.se or database/series from tempo-db.com.
The tempo-db.com 'database' must have been defined in the tempodb/databases section of the configuration.

<pre>
topics:
    /raw/sensor/battery: 45243/battery
</pre>

## Running it

The utils stay resident as a daemons. You can start them, stop them or restart them (to reload the configuration) by using:

<pre>python mqtt2cosm.py start|stop|restart</pre>
<pre>python mqtt2tempodb.py start|stop|restart</pre>



