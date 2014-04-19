import logging
import numpy as np
import cv2

capture = cv2.VideoCapture(1)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001);

while (True):
    # Capture frame-by-frame
    ret, frame = capture.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    minimum = np.min(gray)
    maximum = np.max(gray)
    normalized = (gray - minimum) * (255 / (maximum - minimum))

    ret, corners = cv2.findChessboardCorners(normalized, (7,7), None);
    if ret == True:
        # cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        cv2.drawChessboardCorners(frame, (7,7), corners, ret)

    print ret
    cv2.imshow('gray-img', gray)
    cv2.imshow('normalized-img', normalized)
    cv2.imshow('color-img', frame)


# When everything done, release the capture
capture.release()
cv2.destroyAllWindows()
