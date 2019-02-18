import time
import random
import paho.mqtt.client as mqtt
import numpy as np

def on_connect(client, userdata, flags, rc):
    print("Connected with Code:"+str(rc))
    client.subscribe("Home/Control/Boiler")
    
def on_message(client, userdata, msg):
    global boiler
    boiler = int(msg.payload)
    print("boiler: " + str(boiler))

boiler = 0

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("", "")
client.connect("m20.cloudmqtt.com", 00000, 60)

client.loop_start()

temp_t = 15
temp_e = 5
b = 0

while True:
	if (boiler==1):
		if(temp_t<70):
			b = np.log(np.exp(70-temp_t) + np.exp(temp_e))*0.001
		else:
			b=0
	else:
		if(temp_t > temp_e):
			b = -0.025*np.power((temp_t-temp_e), 0.3)
		else:
			b=0
    
	temp_t += b+ (random.randint(0,5)*0.05 - 0.125)
	
    
	client.publish("Home/Sensor/Temp", temp_t)
	print(temp_t)
	time.sleep(3)

client.loop_stop()

client.disconnect()

