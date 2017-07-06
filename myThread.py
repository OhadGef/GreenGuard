from camera import camera
import threading


class MyThread:

    def __init__(self):
        print ("[init My Tread class]")
        self.cameraId = "1136485950"
        # self.cameraId = uuid.uuid4().int & (1<<32)-1
        print ("camera id: " ,self.cameraId)
        self.createTread()
        # self.createTread()
        return

    def createTread(self):
        print ('[Tread crated]')
        self.stopEvent = threading.Event()
        self.cam1 = camera(self.cameraId)
        self.cameraTread = threading.Thread(target=self.cam1.run, args=(self.stopEvent,))

    def startCamera(self):
        print ('[Camera started ]')
        print (threading.enumerate())

        try:
            self.cameraTread.start()
        except:
            self.createTread()
            self.cameraTread.start()

        return

    def stop(self):
        print (threading.enumerate())
        print (threading.active_count())
        self.stopEvent.set()
        self.cameraTread.join(1)
        print (threading.enumerate())
        print (threading.active_count())
        del self.cameraTread
        del self.cam1
        del self.stopEvent
        print ("[camera stopped]")
        return
