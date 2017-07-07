
from picController.pictureSaverAndSender import pictureSaverAndSender
import datetime
import json
import time
import cv2
import numpy as np
import uuid

class camera():
    def __init__(self,cameraId):
        self.cameraId = cameraId
        self.cameraInitialise()
        self.pictureSaverAndSender = pictureSaverAndSender()
        return

    def cameraInitialise(self):
        print ('[camera initialized]')
        camera = cv2.VideoCapture(0)
        # camera = cv2.VideoCapture("./carInThePool.avi")
        time.sleep(2)
        status,frame = camera.read()
        if(status):
            cv2.imwrite("picController/img/frame-1.jpg", frame)
            self.status = 10
            return 10
        else:
            self.status = 11
            return 11


    def run(self,  stop_event ):
        rule = json.load(open('theRule.json'))
        self.myPolygon = np.array(rule["polygon"])
        self.inOut = rule['inOut']
        conf = json.load(open('conf.json'))
        # rule= json.load(open('theRule.json'))
        # myArray = np.array(rule["polygon"])

        self.cameraRun = cv2.VideoCapture(0)
        # allow the camera to warmup, then initialize the average frame, last
        time.sleep(2)
        # camera = cv2.VideoCapture("./carInThePool.avi")
        # uploaded timestamp, and frame motion counter
        print ("[INFO] warming up...")

        avg = None
        # lastUploaded = datetime.datetime.now()
        lastUploaded = datetime.datetime.now()
        eventNumber = uuid.uuid4().int & (1<<32)-1
        # eventNumber = 0


        # capture frames from the camera
        # for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        while not stop_event.is_set():
            ret, frame = self.cameraRun.read()
            # grab the raw NumPy array representing the image and initialize
            # the timestamp and Alert/Ok text
            # frame = f.array
            timestamp = datetime.datetime.now()
            text = "OK"


            # resize the frame, convert it to grayscale, and blur it
            # frame = imutils.resize(frame, conf["width"])
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the average frame is None, initialize it
            if avg is None:
                print ("[INFO] starting background model...")
                print (timestamp)
                avg = gray.copy().astype("float")

                mask = np.zeros((gray.shape[0], gray.shape[1]), dtype=np.uint8)
                cv2.fillConvexPoly(mask,self.myPolygon, 1)
                mask = mask.astype(np.bool)


            out = np.zeros_like(gray)
            if self.inOut is 1:
                # "looking out of the erea."
                screen = gray
                screen[mask] = out[mask]

            if self.inOut is 0:
                # print "looking in the erea."
                screen = np.zeros_like(gray)
                out[mask] = gray[mask]
                screen[mask] = out[mask]

            else:
                screen = gray

            screenSize = cv2.countNonZero(screen)
            # print ("screenSize:", screenSize)
            screenSize *= 0.02
            # print ("screenSize:", screenSize)

            # accumulate the weighted average between the current frame and
            # previous frames, then compute the difference between the current
            # frame and running average
            cv2.accumulateWeighted(screen, avg, 0.5)
            frameDelta = cv2.absdiff(screen, cv2.convertScaleAbs(avg))

            # threshold the delta image, dilate the thresholded image to fill
            # in holes, then find contours on thresholded image
            thresh = cv2.threshold(frameDelta,  conf["delta_thresh"], 255,cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            im2, cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < screenSize:
                    continue

                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Alert ! ! !"

            # draw the text and timestamp on the frame
            ts = timestamp.strftime("%d-%B-%Y--%I:%M:%S%p")
            cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.35, (0, 0, 255), 1)

            # check to see if there is Alert
            if text == "Alert ! ! !":
                # check to see if enough time has passed between uploads
                if (timestamp - lastUploaded).seconds >=  conf["min_upload_seconds"]:
                    #check to see if enough time has passed between events
                    if (timestamp - lastUploaded).seconds >= conf["min_time_events"]:
                        eventNumber = uuid.uuid4().int & (1<<32)-1
                        # eventNumber += 1

                    fileName = time.time()
                    self.pictureSaverAndSender.createPicture(fileName, frame, eventNumber)                          # create pictuer
                    self.pictureSaverAndSender.sendPicture(self.cameraId)                                           # send picture

                    #printing to control
                    print ("[UPLOAD] {}".format(ts))
                    print(timestamp-lastUploaded)
                    print(eventNumber)


                    lastUploaded = timestamp

            # check to see if the frames should be displayed to screen
            if conf["show_video"]:
                # display the security feed
                cv2.imshow("Security Feed", frame)
                # cv2.imshow("Frame Delta", frameDelta)
                # cv2.imshow('Thresh', thresh)
                # cv2.imshow('screen', screen)

                cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        self.cameraRun.release()
        cv2.destroyAllWindows()

    # def updateRule(self,polygon):
    #     self.myPolygon = polygon
