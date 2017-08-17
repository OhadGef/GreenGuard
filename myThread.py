from camera import camera
import threading
import base64
import cv2


class MyThread:

    def __init__(self):
        print ("[init My Tread class]")

        self.cameraId = "222"

        print ("camera id: " ,self.cameraId)
        self.createTread()
        return

    def createTread(self):
        print ('[Thread crated]')
        self.stopEvent = threading.Event()
        self.cam1 = camera(self.cameraId)
        self.cameraTread = threading.Thread(name='camera-1', target=self.cam1.run, args=(self.stopEvent,))

    def startCamera(self):
        print ('[Camera started ]')
        print ("number of threads:",threading.active_count() ,threading.enumerate())
        print (threading.currentThread().getName())
        try:
            self.cameraTread.start()
        except:
            print ("start createTread()")

            self.createTread()
            self.cameraTread.start()
        return

    def stopCamera(self):
        print (threading.enumerate())
        print (threading.active_count())
        print (threading.currentThread().getName())

        self.stopEvent.set()
        self.cameraTread.join(1)
        print (threading.enumerate())
        print (threading.active_count())
        del self.cameraTread
        del self.cam1
        del self.stopEvent
        print ("[camera stopped]")
        return

    def savePic(self):
        try:

            t,pic = self.cam1.cameraRun.read()
            t,buffer = cv2.imencode('.jpg',pic)
            base64Pic = base64.b64encode(buffer)
            return base64Pic

        except Exception as err:
            print (err)

    def activeThreads (self):

        return threading.active_count()