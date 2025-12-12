import paho.mqtt.client as mqtt
import json
import time
import warnings ; warnings.warn = lambda *args,**kwargs: None

THINGSBOARDEDGEHOST = "localhost"
ACCESSTOKEN = "c5dyeIRgDv6S2K7NtDFx"

sensorData = {'temperature': 25}
currentTemperature = sensorData['temperature']
deviceName = "Thermostat"
PORT = 11883

def getTemperature():
    temp = sensorData['temperature']
    return temp

def setTemperature(params):
    sensorData['temperature'] = params

#Update Temperature Function. Left unused
def updateTemperature(params):
    targetTemperature = params
    step = 5

    if currentTemperature < targetTemperature:
        sensorData['temperature'] = min(sensorData['temperature'] + step, targetTemperature)
    elif sensorData['temperature'] > targetTemperature:
        sensorData['temperature'] = max(sensorData['temperature'] - step, targetTemperature)

    if sensorData['temperature'] != targetTemperature:
        if sensorData['temperature'] > targetTemperature:
            print(f"{deviceName} current temperature: {sensorData['temperature']} °C. Cooling down!")
        elif sensorData['temperature'] < targetTemperature:
            print(f"{deviceName} current temperature: {sensorData['temperature']} °C. Heating up!")
        elif sensorData['temperature'] == targetTemperature:
            print(f"{deviceName} is a temperature: {sensorData['temperature']} °C")

def mqttConnect(client, userdata, flags, rc):
    client.subscribe('v1/devices/me/rpc/request/+')

def rpcMessageRequest(client, userdata, msg):
    if msg.topic.startswith("v1/devices/me/rpc/request/"):
        requestID = msg.topic[len("v1/devices/me/rpc/request/"):len(msg.topic)]
        data = json.loads(msg.payload)

        if data['method'] == "setValue":
            params = float(data['params'])
            setTemperature(params)
            print("Temperature has been updated to: ", params, "°C")

            # Send RPC response back
            client.publish(f"v1/devices/me/rpc/response/{requestID}", json.dumps({"status": "ok"}), 1)

        elif data['method'] == "getValue":
            getTemperature()
            client.publish(f"v1/devices/me/rpc/response/{requestID}", json.dumps(sensorData['temperature']), 1)

#Publishes the devices telemetry at a 5 second interval
def sendTelemetry():
    client.publish("v1/devices/me/telemetry", json.dumps(sensorData))

client = mqtt.Client()
client.username_pw_set(ACCESSTOKEN)

client.on_connect = mqttConnect
client.on_message = rpcMessageRequest

client.connect(THINGSBOARDEDGEHOST, PORT, 60)
client.loop_start()

while True:
    sendTelemetry()
    time.sleep(5)