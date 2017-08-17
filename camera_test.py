from camera import camera
# from webService import webService
from myThread import MyThread
from twisted.internet import reactor

import uuid


def main():

    # start the camera and make first image
    camera = MyThread()
    camera.startCamera()


if __name__ == "__main__":
    main()


