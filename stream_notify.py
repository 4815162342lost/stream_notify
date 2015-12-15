#!/usr/bin/python3.4
import requests
import json
import time
import notify2
from gi.repository.GdkPixbuf import Pixbuf
import os

#for key, value in data.items():
#    stream_id=key
def check_online(streamer_name,pb, index):
    params={"id": streamer_name, "fmt": "json"}
    r=requests.get("http://goodgame.ru/api/getchannelstatus", params=params )
    data=json.loads(r.text)
    print("i am worked")
    for key in data.keys():
        stream_id=key
    if (data[stream_id]['status'])!="Dead":
        if online[index]!=1:
            streamer=data[stream_id]['key']+ ' начал трансляцию'
            game="по игре "+'<b>'+data[stream_id]['games']+'</b>.'
            notify2.init('app_name')
            n = notify2.Notification(streamer, game)
            n.set_timeout(15000)
            n.set_icon_from_pixbuf(pb)
            n.show()
        online[index]=1
    elif (data[stream_id]['status'])=="Dead":
        online[index]=0 

streamers_file=open(os.path.expanduser("~/.config/stream_notify/config"))
mystreamers=[]
online=[]
logo=[]
index=1
for line in streamers_file.readlines():
    line=line[line.find("channel/")+8:-2]
    mystreamers.append(line)
    online.append(0)
    logo.append(Pixbuf.new_from_file(os.path.expanduser("~/.config/stream_notify/")+str(index)+".jpg"))
    index+=1
streamers_file.close()
while True:
    index=0
    for i in mystreamers:
        check_online(i,logo[index], index)
        index+=1
    time.sleep(300)
