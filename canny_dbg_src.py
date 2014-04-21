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

bwphoto = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
cv2.imshow("Grayscale", bwphoto)

minimum = np.min(bwphoto)
maximum = np.max(bwphoto)
bwphoto = (bwphoto - minimum) * (255 / (maximum - minimum))
cv2.imshow("Normalized", bwphoto)

canny = cv2.Canny(bwphoto, 200, 250)
cv2.imshow("Canny", canny)

def line_ok(rho, theta):
    # if abs(rho - 250) > 200:
        # return False
    tol = 5 * np.pi / 180
    if theta <= tol or theta >= (np.pi - tol):
        return True
    if theta >= (np.pi/2 - tol) and theta <= (np.pi/2 + tol):
        return True
    return False

seen_lines = [ ]
def line_duplicate(rho, theta):
    global seen_lines
    dtol = 5
    atol = 5 * np.pi / 180
    for (r, t) in seen_lines:
        if abs(rho - r) <= dtol and abs(theta - t) <= atol:
            return True
    seen_lines += [(rho, theta)]
    return False

lines = cv2.HoughLines(canny, 1, np.pi/180, 120)
final_lines = [ ]
for rho, theta in lines[0]:
    c = np.cos(theta)
    s = np.sin(theta)
    x0 = c * rho
    y0 = s * rho
    x1 = int(x0 - 1000 * s)
    y1 = int(y0 + 1000 * c)
    x2 = int(x0 + 1000 * s)
    y2 = int(y0 - 1000 * c)
    if line_ok(rho, theta):
        if not line_duplicate(rho, theta):
            cv2.line(photo, (x1,y1), (x2,y2), (0,255,0), 1)
            final_lines += [ (abs(rho - 250), x1, y1, x2, y2) ]
        else:
            cv2.line(photo, (x1,y1), (x2,y2), (255,0,0), 1)
    else:
        cv2.line(photo, (x1,y1), (x2,y2), (0,0,255), 1)

final_lines.sort()
for dist, x1, y1, x2, y2 in final_lines[0:18]:
    cv2.line(photo, (x1,y1), (x2,y2), (0,255,255), 3)

cv2.imshow("Result", photo)

cv2.waitKey()
