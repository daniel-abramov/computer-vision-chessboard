#!/usr/bin/env python

import sys
import numpy as np
import cv2

DEBUG = False

if (len(sys.argv) > 1):
    image_name = sys.argv[1]
    print image_name

    if (len(sys.argv) > 2):
        if (sys.argv[2]) != 0:
            DEBUG = True
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

# canny = cv2.Canny(bwphoto, 20, 350)
canny = cv2.Canny(bwphoto, 100, 200)
cv2.imshow("Canny", canny)


width, height = bwphoto.shape
half_size = width / 2

def line_ok(rho, theta):
    # if abs(rho - half_size) > 200:
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
    dtol = 25
    atol = 5 * np.pi / 180
    for (r, t) in seen_lines:
        if abs(rho - r) <= dtol and abs(theta - t) <= atol:
            return True
    seen_lines += [(rho, theta)]
    return False

lines = cv2.HoughLines(canny, 1, np.pi/180, 120)
final_lines = [ ]
for rho, theta in lines[0]:
    if line_ok(rho, theta):
        if not line_duplicate(rho, theta):
            final_lines += [ (rho, theta) ]

final_lines.sort(key = lambda (rho, theta): abs(rho - half_size))
horizontals = [ ]
verticals = [ ]
for rho, theta in final_lines[0:18]:
    if theta < np.pi / 4 or theta > 3 * np.pi * 4:
        verticals += [ (rho, theta) ]
    else:
        horizontals += [ (rho, theta) ]
horizontals.sort()
verticals.sort()

print(len(horizontals))
print(len(verticals))

cv2.waitKey()

upper = horizontals[0]
lower = horizontals[8]
left = verticals[0]
right = verticals[8]

def intersect((rho1, theta1), (rho2, theta2)):
    # rho1 = x * cos(theta1) + y * sin(theta1)
    # rho2 = x * cos(theta2) + y * sin(theta2)
    A = [ [np.cos(theta1), np.sin(theta1)], [np.cos(theta2), np.sin(theta2)] ]
    B = [ rho1, rho2 ]
    # A * (x, y) = B
    return tuple(np.linalg.solve(A, B))


ul = intersect(upper, left)
ur = intersect(upper, right)
ll = intersect(lower, left)
lr = intersect(lower, right)

cv2.line(photo, ul, ur, (0,255,0), 3)
cv2.line(photo, ul, ll, (0,255,0), 3)
cv2.line(photo, ur, lr, (0,255,0), 3)
cv2.line(photo, ll, lr, (0,255,0), 3)

for line in verticals[1:8]:
    cv2.line(photo, intersect(line, upper), intersect(line, lower), (0,255,0), 2)

for line in horizontals[1:8]:
    cv2.line(photo, intersect(line, left), intersect(line, right), (0,255,0), 2)

points = np.zeros((9,9,2))
x = 0
for ver in verticals:
    y = 0
    for hor in horizontals:
        p = intersect(ver, hor)
        cv2.circle(photo, p, 2, (0,0,255), 2)
        points[x, y, : ] = p
        y += 1
    x += 1

# 0 = empty, 1 = white, 2 = black
def detect(img, l, r, u, b, is_black):
    cell = img[ u+5:b-5, l+5:r-5 ]
    deviation = np.std(cell)
    if (deviation < 5):
        # nothing
        return 0
    if (deviation > 50):
        # white on black or black on white
        if is_black:
            return 1
        else:
            return 2
    else:
        # white on white or black on black
        if is_black:
            return 2
        else:
            return 1

black = False
for x in xrange(8):
    for y in xrange(8):
        (x11, y11) = points[x, y, : ]
        (x12, y12) = points[x+1, y, : ]
        (x21, y21) = points[x, y+1, : ]
        (x22, y22) = points[x+1, y+1, : ]
        l = int(max(x11, x21))
        r = int(min(x12, x22))
        u = int(max(y11, y12))
        b = int(min(y21, y22))
        found = detect(bwphoto, l, r, u, b, black)
        cc = ((l + r) / 2, (u + b) / 2)
        if found > 0:
            if found == 1:
                cv2.circle(photo, cc, 5, (255,0,255), 10)
            else:
                cv2.circle(photo, cc, 5, (255,0,0), 10)
        else:
            cv2.circle(photo, cc, 10, (255,0,0), 1)
        black = not black
    black = not black

cv2.imshow("Result", photo)

cv2.waitKey()
