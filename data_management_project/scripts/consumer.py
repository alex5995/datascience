#CONSUMER
from kafka import KafkaConsumer
import json
import time
import datetime
from pymongo import MongoClient

client = MongoClient()
db = client.prograi #inserire il nome del db

consumer = KafkaConsumer(bootstrap_servers='sandbox.hortonworks.com:6667', auto_offset_reset='earliest', consumer_timeout_ms=1000)

consumer.subscribe(['rai1']) #inserire il nome del topic

while(True):
	for message in consumer:
		try:
			messaggio = json.loads(message.value)
			ora = messaggio['created_at']
			ora = datetime.datetime.strptime(ora, "%Y-%m-%d %H:%M:%S")
			ora = time.mktime(ora.timetuple()) + 7200
			ora = datetime.datetime.fromtimestamp(ora).strftime("%Y-%m-%d %H:%M:%S")
			messaggio['created_at'] = ora
			db.rai1.insert_one(messaggio) #inserire il nome della collection
		except:
			print("errore")
	time.sleep(5)
