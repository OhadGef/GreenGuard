from klein import Klein
import json
import requests
import ipgetter
import socket
import os
import time
from myThread import MyThread
from twisted.internet import reactor
from webConfig import *


class webService:

    def __init__(self):
        self.camera = MyThread()
        self.cameraId = self.camera.cameraId
        self.port = "3101"
        self.ip = socket.gethostbyname(socket.gethostname())             # internal ip
        # self.ip = ipgetter.myip()                                      # external ip
        self.camaraRun = False
        self.initialise()

        return

    def initialise(self):
        confAnalysis = {}
        confAnalysis["cameraId"] = self.cameraId
        confAnalysis["ip"] = self.ip
        confAnalysis["port"] = self.port
        confAnalysis["time"] = int(time.time())

        if not os.path.exists('picController/img'):
            os.makedirs('picController/img')

        file = {'file':open("picController/img/frame-1.jpg", "rb")}
        send = serverIp+'/api/cameras/newCamera'
        # send = 'https://green-guard.herokuapp.com/api/cameras/newCamera'
        print (send)
        # res = requests.post(send,data =confAnalysis)

        res = requests.post(send,data =confAnalysis,files = file)

        # self.connectionStatus = res
        return

    def webService(self):
        app = Klein()
        print ("web service starting...")

        with app.subroute("") as app:
            @app.route("/setRule", methods=['POST'])
            def connectCamera(request):
                numberOfThreads = self.camera.testThreads()
                print (numberOfThreads)
                if (numberOfThreads == 1):
                    rule =dict()
                    data = json.loads(request.content.read())
                    print (data)
                    rule["inOut"] = data["inOut"]
                    polygon = []
                    for i in range(len(data['polygon'])):
                        polygon.append([int(data['polygon'][i]['x']), int(data['polygon'][i]['y'])])
                    rule['polygon'] = polygon
                    file=open('theRule.json','w')
                    file.seek(0)
                    json.dump(rule,file)
                    file.close()

                    return "the rule was saved"
                elif (numberOfThreads == 3):
                    self.camera.stop()
                    rule = dict()
                    data = json.loads(request.content.read())
                    print (data)
                    rule["inOut"] = data["inOut"]
                    polygon = []
                    for i in range(len(data['polygon'])):
                        polygon.append([int(data['polygon'][i]['x']), int(data['polygon'][i]['y'])])
                    rule['polygon'] = polygon
                    file = open('theRule.json', 'w')
                    file.seek(0)
                    json.dump(rule, file)
                    file.close()
                    self.camera.startCamera()



            @app.route("/startCamera")
            def startCamera(request):

                try:
                    if( os.path.isfile("theRule.json" ) and self.camaraRun==False ):
                        reactor.callInThread(self.camera.startCamera)
                        self.camaraRun = True
                        return

                except Exception as err:
                    print err


            @app.route("/getLivePicture")
            def getLivePicture(request):
                request.setHeader('Content-Type','application/json')
                pic = self.camera.savePic()
                print "[send Live Picture ]"
                return json.dumps({'pic': pic})


            @app.route("/test")
            def test(request):
                print self.camera.cameraTread.isAlive()
                return "OK OK"


            @app.route("/stop")
            def stop(request):
                self.camaraRun = True
                return self.camera.stop()

        app.run("", self.port)

webService().webService()