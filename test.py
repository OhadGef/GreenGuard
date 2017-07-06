import cv2
import numpy as np

frame = cv2.imread("white.jpg")
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
BLUE_MIN = np.array([1,1], np.uint8)
BLUE_MAX = np.array([50, 50], np.uint8)

# dst = cv2.inRange(gray, BLUE_MIN, BLUE_MAX)
no_blue = cv2.countNonZero(gray)
print('The number of blue pixels is: ' + str(no_blue))
print gray.shape
print BLUE_MIN.shape
cv2.imshow("opencv",gray)
cv2.waitKey(0)