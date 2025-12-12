import paho.mqtt.client as mqtt
import json
import time
import warnings ; warnings.warn = lambda *args,**kwargs: None

THINGSBOARDEDGEHOST = "localhost"
PORT = 11883
ACCESSTOKEN = "wktjA0TXnB8ETEWLcyeH"
value = {'Open': False}

def getState():
    return value['Open']

def setState(params):
    value['Open'] = params
    if value['Open'] == True:
        print("Door is Open")
    else:
        print("Door is Closed")

def mqttConnect(client, userdata, flags, rc):
    client.subscribe('v1/devices/me/rpc/request/+')

def rpcMessageRequest(client, userdata, msg):
    if msg.topic.startswith("v1/devices/me/rpc/request/"):
        requestID = msg.topic[len("v1/devices/me/rpc/request/"):len(msg.topic)]
        data = json.loads(msg.payload)

        if data['method'] == "setState":
            params = data['params']
            setState(params)
            client.publish(f"v1/devices/me/rpc/response/{requestID}", json.dumps({"Open": value['Open']}), 1)

        elif data['method'] == "getState":
            getState()
            client.publish(f"v1/devices/me/rpc/response/{requestID}", json.dumps(value['Open']), 1)

#Publishes the devices telemetry at a 2 second interval
def sendTelemetry():
    client.publish("v1/devices/me/telemetry", json.dumps({"Open": value['Open']}))

client = mqtt.Client()
client.username_pw_set(ACCESSTOKEN)

client.on_connect = mqttConnect
client.on_message = rpcMessageRequest

client.connect(THINGSBOARDEDGEHOST, PORT, 60)
client.loop_start()

while True:
    sendTelemetry()

    time.sleep(2)
