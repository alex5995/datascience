import time
import random
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with Code:"+str(rc))
    client.subscribe("Home/Control/#")
    
def on_message(client, userdata, msg):
	if msg.topic == "Home/Control/Status/Richieste":
		global status_required
		status_required = 1
		print("Ho ricevuto la richiesta")
	elif msg.topic == "Home/Control/Boiler":
		global status
		status = float(msg.payload)
		print("Boiler: " + str(status))

status = 0
status_required = 0

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("", "")
client.connect("m20.cloudmqtt.com", 00000, 60)

client.loop_start()

while True:
	if status_required == 1:
		client.publish("Home/Control/Status/Risposte", status)
		status_required = 0
	
	time.sleep(3)
client.loop_stop()

client.disconnect()