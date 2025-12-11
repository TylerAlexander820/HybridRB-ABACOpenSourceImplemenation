import paho.mqtt.client as mqtt
import json
import time
import warnings ; warnings.warn = lambda *args,**kwargs: None

THINGSBOARDEDGEHOST = "localhost"

ACCESSTOKEN = "TRJYSQwCjUSiBAkKDS3r"
value = {'value': False}
PORT = 11883

def getValue():
    return value['value']

def setValue(params):
    value['value'] = bool(params)

def on_connect(client, userdata, flags, rc):
    #print("Connected with result code", rc)
    client.subscribe('v1/devices/me/rpc/request/+')

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
            getValue()
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
    time.sleep(5)