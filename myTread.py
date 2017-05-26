import uuid
from camera import camera
from threading import Thread


class MyTread:
    def __init__(self):
        print ("init my tread")
        # self.cameraId = uuid.uuid4().hex
        self.cameraId = uuid.uuid4().int & (1<<32)-1
        print self.cameraId
        cam1= camera(self.cameraId)
        self.cameraStart = Thread(target=cam1.analysis)
        return

    def createCamera(self):
        print ('createCamera')
        self.cameraStart.start()
        return

    def closeCamera(self):
        print ("close camera")
        self.cameraStart.join()
        print (self.cameraStart.isAlive())
        return


