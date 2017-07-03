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
        self.port = "3100"
        self.ip = socket.gethostbyname(socket.gethostname())             # internal ip
        # self.ip = ipgetter.myip()                                      # external ip
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

            @app.route("/startCamera")
            def startCamera(request):
                if ( os.path.isfile("theRule.json" )):
                    reactor.callInThread(self.camera.startCamera)
                else:
                    print ("there is no Rule for the camera")
                return

            @app.route("/getLifePicture",methods=['POST'])
            def getLifePicture(request):
                return

            @app.route("/test")
            def test(request):
                return "OK OK"

            @app.route("/stop")
            def stop(request):
                return self.camera.stop()

        app.run("", self.port)

webService().webService()