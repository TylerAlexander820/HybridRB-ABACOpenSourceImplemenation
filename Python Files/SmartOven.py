import paho.mqtt.client as mqtt
import json
import time
import warnings ; warnings.warn = lambda *args,**kwargs: None

THINGSBOARDEDGEHOST = "localhost"
ACCESSTOKEN = "KEkN2bvIe0ij4wCE7dLp"
ovenData = {'ovenState': False, 'temperature': 0}
PORT = 11883
deviceName = "Oven"

def getValue():
    temp = ovenData['temperature']
    return temp

def setValue(params):
    ovenData['temperature'] = params
    print("Temperature is now: ", params, "°C")

def getState(params):
    ovenState = ovenData['ovenState']
    return ovenState

def setState(params):
    ovenData['ovenState'] = params
    if (params == True):
        print("Oven is now on")
    else:
        ovenData['temperature'] = 0
        print("Oven is now off")

#Left unused
def updateTemperature(params):
    targetTemperature = params
    step = 5

    if ovenData < targetTemperature:
        ovenData['temperature'] = min(ovenData['temperature'] + step, targetTemperature)
    elif ovenData['temperature'] > targetTemperature:
        ovenData['temperature'] = max(ovenData['temperature'] - step, targetTemperature)

    if ovenData['temperature'] != targetTemperature:
        if ovenData['temperature'] > targetTemperature:
            print(f"{deviceName} current temperature: {ovenData['temperature']} °C. Cooling down!")
        elif ovenData['temperature'] < targetTemperature:
            print(f"{deviceName} current temperature: {ovenData['temperature']} °C. Heating up!")
        elif ovenData['temperature'] == targetTemperature:
            print(f"{deviceName} is a temperature: {ovenData['temperature']} °C")

def mqttConnect(client, userdata, flags, rc):
    client.subscribe('v1/devices/me/rpc/request/+')

def rpcMessageRequest(client, userdata, msg):
    if msg.topic.startswith("v1/devices/me/rpc/request/"):
        requestID = msg.topic[len("v1/devices/me/rpc/request/"):len(msg.topic)]
        data = json.loads(msg.payload)

        #Sets temperature value
        if data['method'] == "setValue":
            params = float(data['params'])
            setValue(params)
            # Publishes RPC response
            client.publish(f"v1/devices/me/rpc/response/{requestID}", json.dumps({"status": "ok"}), 1)

        elif data['method'] == "getValue":
            client.publish(f"v1/devices/me/rpc/response/{requestID}", json.dumps(ovenData['temperature']), 1)

        if data['method'] == "setState":
            params = data['params']
            setState(params)
            client.publish(f"v1/devices/me/rpc/response/{requestID}", json.dumps({"status": "ok"}), 1)

        elif data['method'] == "getState":
            getState()
            client.publish(f"v1/devices/me/rpc/response/{requestID}", json.dumps(ovenData['ovenState']), 1)

#Publishes the devices telemetry at a 2 second interval
def sendTelemetry():
    client.publish("v1/devices/me/telemetry", json.dumps(ovenData))

client = mqtt.Client()
client.username_pw_set(ACCESSTOKEN)

client.on_connect = mqttConnect
client.on_message = rpcMessageRequest

client.connect(THINGSBOARDEDGEHOST, PORT, 60)
client.loop_start()

while True:
    sendTelemetry()
    time.sleep(5)