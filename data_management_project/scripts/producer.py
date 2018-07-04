#PRODUCER
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
import time
import datetime
import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='sandbox.hortonworks.com:6667')

consumer_key=""
consumer_secret=""

access_token=""
access_token_secret=""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class Listener(tweepy.StreamListener):
	def __init__(self, time_limit=0, name_event="", inizio=0, orario_inizio="", orario_fine="", key=""):
		self.start_time = inizio
		self.limit = time_limit
		self.event = name_event
		self.inizio = orario_inizio
		self.fine = orario_fine
		self.key = key
		super(Listener, self).__init__()
        
	def on_status(self, status):
		if (time.time() +7200 - self.start_time) < self.limit:
			diz = {'screen_name':status.user.screen_name,
			'created_at':str(status.created_at),
			'followers':status.user.followers_count,
			'friends':status.user.friends_count,
			'text':status.text,
			'hashtag':status.entities['hashtags'],
			'nome_evento':self.event,
			'orario_inizio':self.inizio,
			'orario_fine':self.fine,
			'keywords':self.key
			}
			producer.send('rai1', json.dumps(diz)) #inserire il nome del topic
			return True
		else:
			return False
        
	def on_error(self, status):
		print('Error on status')
        
	def on_limit(self, status):
		print('Limit threshold exceeded')
    
	def on_timeout(self, status):
		print('Stream disconnected; continuing...')

f = open("/home/maria_dev/rai1_ok.csv", "r") #inserire il nome del csv
programmi = f.readlines()
for programma in programmi:
	programma = programma.strip("\n\r")
	lista = programma.split(";")
	
	print(lista)
	
	h_in = lista[1]
	h_in = datetime.datetime.strptime(h_in, "%Y-%m-%d %H:%M:%S")
	h_in = time.mktime(h_in.timetuple())

	h_fin = lista[2]
	h_fin = datetime.datetime.strptime(h_fin, "%Y-%m-%d %H:%M:%S")
	h_fin = time.mktime(h_fin.timetuple())

	limit = h_fin - h_in

	ev = lista[0]

	keyword=json.loads(lista[3])
	
	while (time.time()+7200) < h_in:
		time.sleep(5)

	stream = Listener
	stream = Stream(auth = api.auth, listener=stream(time_limit=limit, name_event=ev ,inizio=h_in, orario_inizio=lista[1], orario_fine=lista[2], key=keyword))
	stream.filter(track=keyword, languages=["it"])
f.close()
