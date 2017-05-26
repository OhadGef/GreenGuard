import os,time
import json
import requests
cameraID = 'ID-01'


class sendAlerts:
#loop for check if ther is event
    def __init__(self):
        self.path = 'img/'
    def alerts(self,id):
        while 1:
            events = os.listdir(self.path)
            if len(events) is 1:
                print 'sleep'
                time.sleep(10)

            #loop of events
            for event in range(len(events)):
                if not str(events[event]).endswith(('.jpg')):
                    # if not os.path.exists("img/"+str(events[event])+"/json"):
                    #     os.makedirs("img/"+str(events[event])+"/json")
                    eventsImpgs =  os.listdir(self.path+str(events[event]))
                    for imges in range(len(eventsImpgs)):
                        if str(eventsImpgs[imges]).endswith(('.jpg')):
                            json = {}
                            img_file = {'file':open("img/"+str(events[event])+'/'+str(eventsImpgs[imges]), "rb")}
                            json['alertId'] = events[event]
                            # json['img'] = eventsImpgs[imges]
                            json['date'] = os.path.getctime(self.path+str(events[event])+'/'+str(eventsImpgs[imges]))
                            # json['date'] = time.ctime(os.path.getctime(self.path+str(events[event])+'/'+str(eventsImpgs[imges])))
                            # img_file.close()
                            print json
                            res = requests.post('http://localhost:3000/api/cameras/cameraAlert/'+str(id), data=json, files=img_file)
                            if res.status_code is 200:
                                os.remove("img/"+str(events[event])+'/'+str(eventsImpgs[imges]))
                                print 200
                    if not eventsImpgs:
                        print (str(events[event])+" is empty" )
                        os.rmdir(self.path+str(events[event]))
                        break


