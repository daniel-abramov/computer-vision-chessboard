#!/usr/bin/env python

import sys
import numpy as np
import cv2

if (len(sys.argv) > 1):
    image_name = sys.argv[1]
    print image_name
else:
    print "You haven't passed the image name"
    sys.exit()

photo = cv2.imread(image_name)
cv2.imshow("Original", photo)

grayscale = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
cv2.imshow("Grayscale", grayscale)

minimum = np.min(grayscale)
maximum = np.max(grayscale)
normalized = (grayscale - minimum) * (255 / (maximum - minimum))

# cv2.normalize(normalized, normalized, 0, 255, CV_MINIMAX)

cv2.imshow("Normalized", normalized)

ret, corners = cv2.findChessboardCorners(normalized, (7,7), None)
if ret == True:
    print "Chessboard corners has been detected"
    cv2.drawChessboardCorners(photo, (7,7), corners, ret)
else:
    print "Chessboard corners has not been detected"

cv2.imshow('Result', photo)

cv2.waitKey()
cv2.destroyAllWindows()
