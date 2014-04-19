#!/usr/bin/env python

import sys
import numpy as np
import cv2

rows = 7
columns = 7

if (len(sys.argv) > 1):
    image_name = sys.argv[1]
    print image_name

    if (len(sys.argv) == 3):
        dimensions = sys.argv[2]
        rows = int(dimensions[0])
        columns = int(dimensions[2])

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

print 'rows = {0}, columns = {1}'.format(rows, columns)
ret, corners = cv2.findChessboardCorners(normalized, (rows,columns), None)
if ret == True:
    print "Chessboard corners has been detected"
    cv2.drawChessboardCorners(photo, (rows,columns), corners, ret)
else:
    print "Chessboard corners has not been detected"

cv2.imshow('Result', photo)

cv2.waitKey()
cv2.destroyAllWindows()
