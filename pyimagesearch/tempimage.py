# import the necessary packages
import os
import cv2
import requests
class TempImage:
    def __init__(self):
        self.base ="img/"
        self.ext = ".jpg"
        self.serverIp = '192.168.1.11'
        return

    def createPicture(self, fileName, frame, eventNumber):
        # construct the file path
        self.directory = self.base + str(eventNumber)
        self.eventNumber = eventNumber
        self.fileName=fileName
        if not os.path.exists( self.directory):
            # if len(os.listdir(self.base))>2 :
            #     os.rmdir()
            os.makedirs(self.directory)
        self.path = "{path}/{fileName}{ext}".format(path=os.path.join(self.base, str(eventNumber)), fileName=fileName,
                                                    ext=self.ext)
        # print self.path
        print type(frame)
        stringImg = frame.tobytes()
        cv2.imwrite(self.path,frame)

    def sendPicture(self,id):
        events = os.listdir(self.directory)
        # # loop of events
        print events
        if len(events) is 1:
            json = {}
            img_file = {'file': open(self.path, "rb")}
            json['alertId'] = self.eventNumber
            json['cameraId'] = id
            json['time'] = int(self.fileName)
            json['date'] = os.path.getctime(self.path)
            send = 'https://green-guard.herokuapp.com/api/cameras/newCamera'
            # send = 'http://'+self.serverIp+':3000/api/cameras/cameraAlert/'
            # res = requests.post('http://localhost:3000/api/cameras/cameraAlert/', data=json)
            res = requests.post( send + str(id),
                                data=json, files=img_file)




            if res.status_code is 200:
                # os.remove(self.path)
                print '200'
        else:
            json = {}
            img_file = {
                'file': open(self.path, "rb")}
            json['alertId'] = self.eventNumber
            json['cameraId'] = id
            json['time'] = int(self.fileName)
            json['date'] = os.path.getctime(self.path)
            print json
            # res = requests.post('http://'+self.serverIp+':3000/api/cameras/cameraAlertPhoto/' + str(self.eventNumber),
            #                 data=json, files=img_file)
            res = requests.post('https://green-guard.herokuapp.com/api/cameras/cameraAlertPhoto/' + str(self.eventNumber),
                            data=json, files=img_file)

            if res.status_code is 200:
                # os.remove(self.path)
                print '200'
