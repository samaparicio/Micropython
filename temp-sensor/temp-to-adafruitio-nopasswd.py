# Publishes temperature measaured with DHT11 to Adafruit IO
# from https://github.com/MikeTeachman/micropython-adafruit-mqtt-esp8266/blob/master/mqtt-to-adafruit.py

import network
import time
import machine
import dht
from umqtt.simple import MQTTClient
from machine import Pin


# Setup sensor, connected to pin 12 = D6/MISO https://wiki.wemos.cc/products:d1:d1
d = dht.DHT11(machine.Pin(12))

#
# connect the ESP8266 to local wifi network
#
yourWifiSSID = "<yourWifiSSID>"
yourWifiPassword = "<yourWifiPassword>"
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(yourWifiSSID, yourWifiPassword)
while not sta_if.isconnected():
  pass

#
# connect ESP8266 to Adafruit IO using MQTT
#
myMqttClient = "<yourdevicename>"  # can be anything unique
adafruitIoUrl = "io.adafruit.com"
adafruitUsername = "<yourusername>"  # can be found at "My Account" at adafruit.com
adafruitAioKey = "<yourkey>"  # can be found by clicking on "VIEW AIO KEYS" when viewing an Adafruit IO Feed
c = MQTTClient(myMqttClient, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)
c.connect()

#
# publish temperature to Adafruit IO using MQTT
#
# note on feed name in the MQTT Publish:
#    format:
#      "<adafruit-username>/feeds/<adafruitIO-feedname>"
while True:
  d.measure()
  c.publish("samap/feeds/miner-sensors.minertempmonitor1", str(d.temperature()))  # publish temperature to adafruit IO feed
  time.sleep(30)  # number of seconds between each Publish

c.disconnect()
