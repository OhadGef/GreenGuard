from camera import camera
# from webService import webService
import uuid


def main():

    # start the camera and make first image
    cameraId = uuid.uuid4().hex
    cam1 = camera(cameraId)
    print (cam1)


    cam1.analysis()
    # webserviseStatus = webService()
    # webserviseStatus.webService()
    # webserviseStatus = webService(cam1)
    # webserviseStatus.webService()

if __name__ == "__main__":
    main()


