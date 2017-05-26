from klein import Klein
from sendAlerts import sendAlerts
# from camera import camera

import json
import requests
import ipgetter
import socket
import os
import time
from myTread import MyTread

class webService:

    def __init__(self):
        self.serverIp = '192.168.1.11'
        self.camera = MyTread()
        self.cameraId = self.camera.cameraId
        self.port = "3100"
        # self.ip = socket.gethostbyname(socket.gethostname())             # internal ip
        self.ip = ipgetter.myip()                                      # external ip
        self.initialise()
        # self.cameraStart = Thread(target=camera.analysis)
        # self.sendAlert = Thread(target=sendAlerts().alerts,args=(self.cameraId,))
        return

    def initialise(self):
        confAnalysis = {}
        confAnalysis["cameraId"] = self.cameraId
        confAnalysis["ip"] = self.ip
        confAnalysis["port"] = self.port
        confAnalysis["time"] = int(time.time())

        file = {'file':open("img/frame-1.jpg", "rb")}
        # send = 'http://'+self.serverIp+':3000/api/cameras/newCamera'
        send = 'https://green-guard.herokuapp.com/api/cameras/newCamera'
        print (send)
        # res = requests.post('http://'+self.ip+':3000',data =confAnalysis)
        res = requests.post(send,data =confAnalysis,files = file)
        self.connectionStatus = res
        return self.connectionStatus

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
                    polygon.append([data['polygon'][i]['x'], data['polygon'][i]['y']])
                rule['polygon'] = polygon
                file=open('theRule.json','w')
                file.seek(0)
                json.dump(rule,file)
                file.close()

                # self.cameraStart.start()
                # self.sendAlert.start()
                return "the rule was saved"

            @app.route("/editPolygon")
            def editPolygon(request):
                self.camera.closeCamera()
                # data = json.loads(request.content.read())
                # polygon = []
                # for i in range(len(data['polygon'])):
                #     polygon.append([data['polygon'][i]['y'], data['polygon'][i]['x']])
                return b"bla bla bla."

            # @app.route("/setOrEditInOut")
            # def setOrEditInOut(request):
            #     return b"Pet the polygon array and the rule(External/Internal setings)."
            #
            # @app.route("/getPicture")
            # def getPicture(request):
            #     return b"Pet the polygon array and the rule."
            #
            @app.route("/startCamera")
            def startCamera(request):
                print ('camera start')
                self.camera.createCamera()
                return b"camera started."
            @app.route("/getLifePicture")
            def getLifePicture(request):
                return

            @app.route("/test")
            def test(request):
                return "OK OK`"

        app.run("", self.port)

webService().webService()