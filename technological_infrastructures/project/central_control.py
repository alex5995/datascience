import time
import random
import numpy as np
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
	print("Connected with Code:"+str(rc))
	client.subscribe("Home/#")
	
def on_message(client, userdata, msg):
	global dummy_temp_to_reach
	global dummy_when_to_reach
	global temp_to_reach
	global when_to_reach
	global boiler
	global real_boiler
	global temp_now
	
	if msg.topic == 'Home/Control/Temp':
		dummy_temp_to_reach = float(msg.payload)
		print("dttr: " + str(dummy_temp_to_reach))
	elif msg.topic == 'Home/Control/When':
		dummy_when_to_reach = int(msg.payload)
		print("dwtr: " + str(dummy_when_to_reach))
	elif msg.topic == 'Home/Control/Confirm':	
		try:
			temp_to_reach = dummy_temp_to_reach
			when_to_reach = dummy_when_to_reach
			boiler = -1
			print("temp_to_reach: " + str(temp_to_reach) + " in " + str(when_to_reach))
		except:
			pass
	elif msg.topic == 'Home/Control/Status/Risposte':
		real_boiler = float(msg.payload)	
	elif msg.topic == 'Home/Sensor/Temp':
		temp_now = float(msg.payload)
	

temp_now = 15
temp_to_reach = temp_now
dummy_temp_to_reach = temp_to_reach
when_to_reach = 0
dummy_when_to_reach = when_to_reach
temp_est = 0
boiler = 0
real_boiler = -1
status_wait = -1

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("", "")
client.connect("m20.cloudmqtt.com", 00000, 60)

client.loop_start()

while True:
	if when_to_reach > 0:
		when_to_reach -= 1
	
	if ((boiler == 1) and (temp_now >= temp_to_reach)) or (boiler == -1):
		client.publish("Home/Control/Boiler", 0)
		print("Boiler Off, temp_now=" + str(temp_now) + " and temp_to_reach=" + str(temp_to_reach))
		boiler = 0
		status_wait = 1
	
	if boiler == 0:
		prev = temp_now
		for i in range(when_to_reach):
			prev += np.log(np.exp(70-prev) + np.exp(temp_est))*0.0009
		print("Previsione tra " + str(when_to_reach) + " periodi: " + str(prev))
		if prev <= (temp_to_reach - 1):
			client.publish("Home/Control/Boiler", 1)
			print("Boiler On, prev=" + str(prev) + " and temp_to_reach=" + str(temp_to_reach))
			boiler = 1
			status_wait = 1
			when_to_reach = 0
			
	if status_wait >= 0:
		status_wait -= 1
		if status_wait == 0:
			client.publish("Home/Control/Status/Richieste", "Richiesta")
			print("Richiesto check")
			
	if (real_boiler == 0) and (boiler == 1):
		client.publish("Home/Control/Boiler", 1)
		print("Ho richiesto ancora l'accensione")
		real_boiler = -1
		status_wait = 1
	elif (real_boiler == 1) and (boiler == 0):
		client.publish("Home/Control/Boiler", 0)
		print("Ho richiesto ancora lo spegnimento")
		real_boiler = -1
		status_wait = 1
	elif real_boiler != -1:
		print("Ho verificato che lo stato della caldaia è " + str(real_boiler))
		real_boiler = -1
		

	time.sleep(3)
	
client.loop_stop()

client.disconnect()