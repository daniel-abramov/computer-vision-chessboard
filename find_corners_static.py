#!/usr/bin/env python

import numpy as np
import cv2

photo = cv2.imread("chess-demo-bord-wood2-500x500.jpg")
cv2.imshow("Original", photo)

grayscale = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
cv2.imshow("Grayscale", grayscale)

minimum = np.min(grayscale)
maximum = np.max(grayscale)
normalized = (grayscale - minimum) * (255 / (maximum - minimum))
cv2.imshow("Normalized", normalized)

ret, corners = cv2.findChessboardCorners(normalized, (7,7), None)
if ret == True:
    cv2.drawChessboardCorners(photo, (7,7), corners, ret)
print ret

cv2.imshow('Result', photo)

cv2.waitKey()
cv2.destroyAllWindows()
