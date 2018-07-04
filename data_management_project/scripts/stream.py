from kafka import KafkaConsumer
import json
import time
import heapq

consumer = KafkaConsumer(bootstrap_servers='sandbox.hortonworks.com:6667', auto_offset_reset='earliest', consumer_timeout_ms=1000)
consumer.subscribe(['rai1']) #inserire il nome del topic

diz = {}
i=0
num=100 #ogni quanti tweet visualizzare la classifica degli hashtag
while(True):
	for message in consumer:
		i+=1
		hashtags = json.loads(message.value)['hashtag']		
		for hashtag in hashtags:
			try:
				diz[hashtag['text'].lower()]+=1
			except:
				diz[hashtag['text'].lower()]=1
		if i%num==0:
			print("records: "+str(i)+"\n")
			top10 = heapq.nlargest(10, diz, key=diz.get)
        		for el in top10:
                		print(el+':'+str(diz[el]))
			print("\n")
  
	time.sleep(5)
			
