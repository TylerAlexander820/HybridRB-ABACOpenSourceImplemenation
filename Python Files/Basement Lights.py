import paho.mqtt.client as mqtt
import json
import time
import warnings ; warnings.warn = lambda *args,**kwargs: None

THINGSBOARDEDGEHOST = "localhost"
PORT = 11883
ACCESSTOKEN = "ealg8r3IPjDI5psGhKE8"
value = {'value': False}

#Returns the light's state to the ThingsBoard platform
#def getValue():
   #return value['value']

#Sets the light's state from the received RPC Command
def setValue(params):
    value['value'] = bool(params)

#Connects to the Thingsboard platform through MQTT
def on_connect(client, userdata, flags, rc):
    client.subscribe('v1/devices/me/rpc/request/+')

#Defines what to execute based on the received message
def on_message(client, userdata, msg):
    if msg.topic.startswith("v1/devices/me/rpc/request/"):
        requestID = msg.topic[len("v1/devices/me/rpc/request/"):len(msg.topic)]
        data = json.loads(msg.payload)

        if data['method'] == "setValue":
            params = data['params']
            setValue(params)
            print("Lights are now on" if value['value'] else "Lights are now off")
            client.publish(f"v1/devices/me/rpc/response/{requestID}", json.dumps({"status": "ok"}), 1)

        elif data['method'] == "getValue":
            client.publish(f"v1/devices/me/rpc/response/{requestID}", json.dumps({"value": value['value']}), 1)

#Publishes the devices telemetry at a 2 second interval
def sendTelemetry():
    client.publish("v1/devices/me/telemetry", json.dumps(value))

client = mqtt.Client()
client.username_pw_set(ACCESSTOKEN)

client.on_connect = on_connect
client.on_message = on_message

client.connect(THINGSBOARDEDGEHOST, PORT, 60)
client.loop_start()

while True:
    sendTelemetry()
    time.sleep(2)