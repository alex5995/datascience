from pymongo import MongoClient
import matplotlib.pyplot as plt
client = MongoClient()
db = client.prograi
bcls = db.rai1.find({'nome_evento':'Ballando con le stelle'})
xAx=[]
yAx1=[]
yAx2=[]
yAx3=[]
yAx4=[]
x=0
k1=0
k2=0
k3=0
k4=0
interval=100
plottati=0
plt.plot(xAx,yAx1,'r',label="edio") #keyword1
plt.plot(xAx,yAx2,'b',label="scanudivano") #keyword2
plt.plot(xAx,yAx3,'g',label="akashkumar") #keyword3
plt.plot(xAx,yAx4,'y',label="sandromayer") #keyword4
plt.legend(loc='upper left')
plt.title("Real Time Keywords")
plt.xlabel("Tweet analizzati")
plt.ylabel("Frequenza keyword")
for post in bcls:
    x+=1
    hashtags = post['hashtag']
    for hashtag in hashtags:
        if hashtag['text'].lower() == "edio":
            k1+=1
        elif hashtag['text'].lower() == "scanudivano":
            k2+=1
        elif hashtag['text'].lower() == "akashkumar":
            k3+=1
        elif hashtag['text'].lower() == "sandromayer":
            k4+=1
    xAx.append(x)
    yAx1.append(k1)
    yAx2.append(k2)
    yAx3.append(k3)
    yAx4.append(k4)
    if ((x>=interval)&(x%interval==0)):
        plottati=x-interval-1
        plt.plot(xAx[plottati:],yAx1[plottati:],'r')
        plt.plot(xAx[plottati:],yAx2[plottati:],'b')
        plt.plot(xAx[plottati:],yAx3[plottati:],'g')
        plt.plot(xAx[plottati:],yAx4[plottati:],'y')
        plt.pause(0.05)
plt.pause(60)