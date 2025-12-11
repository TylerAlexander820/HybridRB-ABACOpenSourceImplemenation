import paho.mqtt.client as mqtt
import json
import time
import warnings ; warnings.warn = lambda *args,**kwargs: None

THINGSBOARDEDGEHOST = "localhost"
PORT = 11883
ACCESSTOKEN = "XzsVq13PiKeP1vkKJCDr"
value = {'On': 'false'}

def getState():
    lightState = value['Open']
    return lightState

def setState(params):
    value['On'] = params
    if value['On'] == True:
        print("HVAC System is on")
    else:
        print("HVAC System is off")

def on_connect(client, userdata, flags, rc):
    #print("Connected with result code", rc)
    client.subscribe('v1/devices/me/rpc/request/+')

def on_message(client, userdata, msg):
    #print(msg.topic + " " + str(msg.payload))
    if msg.topic.startswith("v1/devices/me/rpc/request/"):
        requestID = msg.topic[len("v1/devices/me/rpc/request/"):len(msg.topic)]
        data = json.loads(msg.payload)

        if data['method'] == "setState":
            params = data['params']
            setState(params)
            client.publish(f"v1/devices/me/rpc/response/{requestID}", json.dumps({"On": value['On']}), 1)

        elif data['method'] == "getState":
            getState()
            client.publish(f"v1/devices/me/rpc/response/{requestID}", json.dumps(value['On']), 1)

#Publishes devices telemetry at a 2 second interval
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